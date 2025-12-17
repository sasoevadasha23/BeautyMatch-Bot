import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class QuestionOption:
    id: str
    text: str
    points: Optional[Dict[str, int]] = None
    hex_color: Optional[str] = None
    image_hint: Optional[str] = None
    makeup_tips: Optional[Dict] = None
    filter_tag: Optional[str] = None

@dataclass
class Question:
    id: str
    order: int
    type: str
    text: str
    description: str
    options: List[QuestionOption]
    required: bool
    max_selections: Optional[int] = None

class QuestionnaireManager:
    def __init__(self, questionnaire_file: str = "data/questionnaire.json"):
        self.questionnaire_file = questionnaire_file
        self.questions = self.load_questionnaire()
    
    def load_questionnaire(self) -> List[Question]:
        """Загружает опросник из JSON файла"""
        try:
            with open(self.questionnaire_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions_data = data['questionnaire']['questions']
            questions = []
            
            for q_data in questions_data:
                options = []
                for opt_data in q_data['options']:
                    option = QuestionOption(
                        id=opt_data['id'],
                        text=opt_data['text'],
                        points=opt_data.get('points'),
                        hex_color=opt_data.get('hex_color'),
                        image_hint=opt_data.get('image_hint'),
                        makeup_tips=opt_data.get('makeup_tips'),
                        filter_tag=opt_data.get('filter_tag')
                    )
                    options.append(option)
                
                question = Question(
                    id=q_data['id'],
                    order=q_data['order'],
                    type=q_data['type'],
                    text=q_data['text'],
                    description=q_data['description'],
                    options=options,
                    required=q_data['required'],
                    max_selections=q_data.get('max_selections')
                )
                questions.append(question)
            
            # Сортируем вопросы по порядку
            questions.sort(key=lambda x: x.order)
            return questions
            
        except FileNotFoundError:
            print(f"Файл {self.questionnaire_file} не найден")
            return []
        except json.JSONDecodeError:
            print("Ошибка при чтении JSON файла")
            return []
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Возвращает вопрос по ID"""
        for question in self.questions:
            if question.id == question_id:
                return question
        return None
    
    def get_next_question(self, current_question_id: str) -> Optional[Question]:
        """Возвращает следующий вопрос"""
        current_question = self.get_question_by_id(current_question_id)
        if not current_question:
            return None
        
        current_index = self.questions.index(current_question)
        if current_index + 1 < len(self.questions):
            return self.questions[current_index + 1]
        return None
    
    def format_question_for_telegram(self, question: Question) -> str:
        """Форматирует вопрос для отправки в Telegram"""
        message = f"*{question.text}*\n"
        message += f"_{question.description}_\n\n"
        
        for i, option in enumerate(question.options, 1):
            if question.type == 'multiple_choice_with_image' and option.image_hint:
                message += f"{i}. {option.text} 📷\n"
            else:
                message += f"{i}. {option.text}\n"
        
        if not question.required:
            message += "\n_(Необязательный вопрос)_"
        
        if question.type == 'multiple_select' and question.max_selections:
            message += f"\n\nМожно выбрать до {question.max_selections} вариантов"
        
        return message
    
    def get_option_by_index(self, question: Question, index: int) -> Optional[QuestionOption]:
        """Возвращает вариант ответа по индексу (начиная с 1)"""
        if 1 <= index <= len(question.options):
            return question.options[index - 1]
        return None
    
    def calculate_color_type(self, answers: Dict[str, List[str]]) -> Dict[str, int]:
        """Рассчитывает баллы для каждого цветотипа на основе ответов"""
        scores = {
            'winter': 0,
            'spring': 0,
            'summer': 0,
            'autumn': 0
        }
        
        for question_id, selected_options in answers.items():
            question = self.get_question_by_id(question_id)
            if not question:
                continue
            
            for option_id in selected_options:
                option = next((opt for opt in question.options if opt.id == option_id), None)
                if option and option.points:
                    for color_type, points in option.points.items():
                        scores[color_type] += points
        
        return scores
    
    def determine_dominant_color_type(self, scores: Dict[str, int]) -> str:
        """Определяет доминирующий цветотип"""
        max_score = max(scores.values())
        dominant_types = [ctype for ctype, score in scores.items() if score == max_score]
        
        if len(dominant_types) == 1:
            return dominant_types[0]
        else:
            # Если несколько цветотипов с одинаковым количеством баллов
            return "mixed"
    
    def get_all_questions_count(self) -> int:
        """Возвращает общее количество вопросов"""
        return len(self.questions)
    
    def get_required_questions_count(self) -> int:
        """Возвращает количество обязательных вопросов"""
        return sum(1 for q in self.questions if q.required)
