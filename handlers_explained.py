"""
handlers_explained.py

Это версия handlers.py, но с подробными комментариями.

Идея бота:
- человек проходит мини-квиз из 5 вопросов
- ответы сохраняются в context.user_data
- потом мы идём в базу данных и ищем товары, у которых массивы подходят под ответы

Порядок вопросов:
1) цвет глаз
2) тон кожи
3) цвет волос
4) форма лица
5) повод

Тут много текста и объяснений, потому что это учебная версия.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database import SessionLocal
from database import (
    Highlighter,
    Lipstick,
    LipGloss,
    Foundation,
    Eyeshadow,
    Mascara,
    Blush,
    Eyeliner,
)


# ConversationHandler работает через "состояния".
# range(5) просто выдаст числа 0..4.
EYE_COLOR, SKIN_TONE, HAIR_COLOR, FACE_SHAPE, OCCASION = range(5)


# Списки вариантов для кнопок.
# Важно: эти значения должны совпадать с тем, что лежит в JSON и в БД.
EYE_COLORS = ["карие", "зеленые", "голубые", "серые", "темные"]
SKIN_TONES = ["светлый", "средний", "темный"]
HAIR_COLORS = ["блондин", "русые", "шатен", "брюнет", "рыжие"]
FACE_SHAPES = ["овальное", "квадратное", "круглое", "треугольное"]
OCCASIONS = [
    "повседневный",
    "офисный",
    "вечерний",
    "особый",
    "летний",
    "натуральный",
    "осенний",
    "зимний",
]


def get_products_by_preferences(
    skin_tone: str,
    eye_color: str,
    hair_color: str,
    face_shape: str,
    occasion: str,
):
    """
    Достаём из базы подходящие продукты.

    В базе поля типа skin_tone, eye_color, hair_color, face_shape, occasion — это массивы.
    Например skin_tone может быть ["светлый", "средний"].

    В Postgres оператор @> означает: "массив содержит".
    То есть:
      skin_tone @> ARRAY['светлый']
    значит: в массиве skin_tone есть значение 'светлый'.

    Алгоритм поиска:
    - сначала ищем совпадение по всем 5 ответам
    - если пусто, ищем по 4 (без occasion)
    - если пусто, ищем по 3 (skin + eye + hair)
    - если пусто, ищем по 2 (skin + eye)
    - если пусто, ищем просто по skin

    Возвращаем словарь:
      { "lipstick": [obj1, obj2], "foundation": [obj1], ... }

    Я беру максимум 2 продукта на категорию.
    """

    db = SessionLocal()
    recommendations = {}

    try:
        # тип -> класс модели (таблица)
        product_types = {
            "highlighter": Highlighter,
            "lipstick": Lipstick,
            "lip_gloss": LipGloss,
            "foundation": Foundation,
            "eyeshadow": Eyeshadow,
            "mascara": Mascara,
            "blush": Blush,
            "eyeliner": Eyeliner,
        }

        for product_type, model_class in product_types.items():
            # Самый строгий поиск: по всем 5 параметрам.
            products = db.query(model_class).filter(
                model_class.skin_tone.op("@>")([skin_tone]),
                model_class.eye_color.op("@>")([eye_color]),
                model_class.hair_color.op("@>")([hair_color]),
                model_class.face_shape.op("@>")([face_shape]),
                model_class.occasion.op("@>")([occasion]),
            ).all()

            # Если ничего не нашли — ищем без повода.
            if not products:
                products = db.query(model_class).filter(
                    model_class.skin_tone.op("@>")([skin_tone]),
                    model_class.eye_color.op("@>")([eye_color]),
                    model_class.hair_color.op("@>")([hair_color]),
                    model_class.face_shape.op("@>")([face_shape]),
                ).limit(2).all()

            # Если и так пусто — ещё мягче.
            if not products:
                products = db.query(model_class).filter(
                    model_class.skin_tone.op("@>")([skin_tone]),
                    model_class.eye_color.op("@>")([eye_color]),
                    model_class.hair_color.op("@>")([hair_color]),
                ).limit(2).all()

            if not products:
                products = db.query(model_class).filter(
                    model_class.skin_tone.op("@>")([skin_tone]),
                    model_class.eye_color.op("@>")([eye_color]),
                ).limit(2).all()

            if not products:
                products = db.query(model_class).filter(
                    model_class.skin_tone.op("@>")([skin_tone]),
                ).limit(2).all()

            if products:
                recommendations[product_type] = products[:2]

        return recommendations
    finally:
        # Сессию надо закрыть, иначе можно получить утечки подключений.
        db.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — просто приветствие."""

    text = (
        "Привет! Я бот для подбора косметики.\n\n"
        "Я задам несколько вопросов и предложу варианты.\n"
        "Нажми /quiz чтобы начать."
    )
    await update.message.reply_text(text)


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Старт квиза.

    Здесь мы:
    - очищаем прошлые ответы (на всякий)
    - показываем кнопки для выбора цвета глаз
    - возвращаем состояние EYE_COLOR
    """

    context.user_data.clear()

    keyboard = []
    for eye_color in EYE_COLORS:
        # callback_data — это то, что придёт обратно при клике.
        keyboard.append(
            [InlineKeyboardButton(eye_color.capitalize(), callback_data=f"eye_{eye_color}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Давай начнем.\n\n"
        "Вопрос 1 из 5:\n"
        "Какой у тебя цвет глаз?",
        reply_markup=reply_markup,
    )

    return EYE_COLOR


async def handle_eye_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Шаг 1 -> 2

    Человек нажал на кнопку с цветом глаз.
    Мы сохраняем ответ и показываем тон кожи.
    """

    query = update.callback_query
    await query.answer()

    # query.data будет например "eye_карие"
    eye_color = query.data.split("_")[1]
    context.user_data["eye_color"] = eye_color

    keyboard = []
    for skin_tone in SKIN_TONES:
        keyboard.append(
            [InlineKeyboardButton(skin_tone.capitalize(), callback_data=f"skin_{skin_tone}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"Цвет глаз: {eye_color.capitalize()}\n\n"
        "Вопрос 2 из 5:\n"
        "Какой у тебя тон кожи?",
        reply_markup=reply_markup,
    )

    return SKIN_TONE


async def handle_skin_tone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Шаг 2 -> 3

    Сохраняем тон кожи и спрашиваем цвет волос.
    """

    query = update.callback_query
    await query.answer()

    skin_tone = query.data.split("_")[1]
    context.user_data["skin_tone"] = skin_tone

    keyboard = []
    for hair_color in HAIR_COLORS:
        keyboard.append(
            [InlineKeyboardButton(hair_color.capitalize(), callback_data=f"hair_{hair_color}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"Цвет глаз: {context.user_data['eye_color'].capitalize()}\n"
        f"Тон кожи: {skin_tone.capitalize()}\n\n"
        "Вопрос 3 из 5:\n"
        "Какой у тебя цвет волос?",
        reply_markup=reply_markup,
    )

    return HAIR_COLOR


async def handle_hair_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Шаг 3 -> 4

    Сохраняем цвет волос и спрашиваем форму лица.
    """

    query = update.callback_query
    await query.answer()

    hair_color = query.data.split("_")[1]
    context.user_data["hair_color"] = hair_color

    keyboard = []
    for face_shape in FACE_SHAPES:
        keyboard.append(
            [InlineKeyboardButton(face_shape.capitalize(), callback_data=f"face_{face_shape}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"Цвет глаз: {context.user_data['eye_color'].capitalize()}\n"
        f"Тон кожи: {context.user_data['skin_tone'].capitalize()}\n"
        f"Цвет волос: {hair_color.capitalize()}\n\n"
        "Вопрос 4 из 5:\n"
        "Какая у тебя форма лица?",
        reply_markup=reply_markup,
    )

    return FACE_SHAPE


async def handle_face_shape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Шаг 4 -> 5

    Сохраняем форму лица и спрашиваем повод (куда макияж).
    """

    query = update.callback_query
    await query.answer()

    face_shape = query.data.split("_")[1]
    context.user_data["face_shape"] = face_shape

    keyboard = []
    for occasion in OCCASIONS:
        keyboard.append(
            [InlineKeyboardButton(occasion.capitalize(), callback_data=f"occasion_{occasion}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"Цвет глаз: {context.user_data['eye_color'].capitalize()}\n"
        f"Тон кожи: {context.user_data['skin_tone'].capitalize()}\n"
        f"Цвет волос: {context.user_data['hair_color'].capitalize()}\n"
        f"Форма лица: {face_shape.capitalize()}\n\n"
        "Вопрос 5 из 5:\n"
        "Для какого повода макияж?",
        reply_markup=reply_markup,
    )

    return OCCASION


async def handle_occasion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Финал.

    Сохраняем повод, подбираем продукты, собираем ответ.
    """

    query = update.callback_query
    await query.answer()

    occasion = query.data.split("_")[1]
    context.user_data["occasion"] = occasion

    recommendations = get_products_by_preferences(
        context.user_data["skin_tone"],
        context.user_data["eye_color"],
        context.user_data["hair_color"],
        context.user_data["face_shape"],
        occasion,
    )

    # Делаем шапку результата.
    result_text = (
        "✨ Твоя подборка:\n"
        "--------------------\n"
        f"👁 Цвет глаз: {context.user_data['eye_color'].capitalize()}\n"
        f"👤 Тон кожи: {context.user_data['skin_tone'].capitalize()}\n"
        f"💇 Цвет волос: {context.user_data['hair_color'].capitalize()}\n"
        f"🙂 Форма лица: {context.user_data['face_shape'].capitalize()}\n"
        f"🎯 Повод: {occasion.capitalize()}\n"
        "--------------------\n\n"
    )

    # Названия категорий + эмодзи, чтобы в ответе было легче читать.
    product_titles = {
        "highlighter": ("✨", "Хайлайтер"),
        "foundation": ("🎨", "Тональный крем"),
        "eyeshadow": ("👁️", "Тени для век"),
        "eyeliner": ("✍️", "Подводка"),
        "mascara": ("👀", "Тушь для ресниц"),
        "blush": ("🩷", "Румяна"),
        "lipstick": ("💄", "Помада"),
        "lip_gloss": ("💋", "Блеск для губ"),
    }

    # recommendations — это словарь, где ключи "тип".
    for product_type, products in recommendations.items():
        if not products:
            continue

        emoji, title = product_titles.get(product_type, ("•", product_type))
        result_text += f"{emoji} {title}\n"
        result_text += "--------------------\n"

        for product in products:
            # product — это объект модели SQLAlchemy.
            result_text += f"• {product.name} — {product.brand}\n"
            result_text += f"  💰 {product.price:.0f} руб.\n"

            # description бывает пустым, поэтому я проверяю.
            if product.description:
                result_text += f"  📝 {product.description}\n"

            result_text += "\n"

    if not recommendations:
        result_text += "😕 Пока ничего не нашлось. Попробуй другие ответы.\n\n"

    result_text += "--------------------\n"
    result_text += "🔄 Хочешь еще раз? Нажми /quiz"

    await query.edit_message_text(result_text)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /cancel — остановить квиз.
    """

    await update.message.reply_text("Ок, отменил. Нажми /start или /quiz.")
    return ConversationHandler.END
