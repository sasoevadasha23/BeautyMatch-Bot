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


EYE_COLOR, SKIN_TONE, HAIR_COLOR, FACE_SHAPE, OCCASION = range(5)

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
    db = SessionLocal()
    recommendations = {}

    try:
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
            products = db.query(model_class).filter(
                model_class.skin_tone.op("@>")([skin_tone]),
                model_class.eye_color.op("@>")([eye_color]),
                model_class.hair_color.op("@>")([hair_color]),
                model_class.face_shape.op("@>")([face_shape]),
                model_class.occasion.op("@>")([occasion]),
            ).all()

            if not products:
                products = db.query(model_class).filter(
                    model_class.skin_tone.op("@>")([skin_tone]),
                    model_class.eye_color.op("@>")([eye_color]),
                    model_class.hair_color.op("@>")([hair_color]),
                    model_class.face_shape.op("@>")([face_shape]),
                ).limit(2).all()

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
        db.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Привет! Я бот для подбора косметики.\n\n"
        "Я помогу найти продукты под твои предпочтения.\n"
        "Нажми /quiz чтобы начать."
    )
    await update.message.reply_text(welcome_text)


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = []
    for eye_color in EYE_COLORS:
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
    query = update.callback_query
    await query.answer()

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

    for product_type, products in recommendations.items():
        if products:
            emoji, title = product_titles.get(product_type, ("•", product_type))
            result_text += f"{emoji} {title}\n"
            result_text += "--------------------\n"
            for product in products:
                result_text += f"• {product.name} — {product.brand}\n"
                result_text += f"  💰 {product.price:.0f} руб.\n"
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
    await update.message.reply_text("Ок, отменил. Нажми /start или /quiz.")
    return ConversationHandler.END

