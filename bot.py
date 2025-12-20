import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from dotenv import load_dotenv

from database import init_db
from handlers import (
    start,
    quiz_start,
    handle_eye_color,
    handle_skin_tone,
    handle_hair_color,
    handle_face_shape,
    handle_occasion,
    cancel,
    EYE_COLOR,
    SKIN_TONE,
    HAIR_COLOR,
    FACE_SHAPE,
    OCCASION,
)

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    init_db()
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('quiz', quiz_start)],
        states={
            EYE_COLOR: [CallbackQueryHandler(handle_eye_color, pattern="^eye_")],
            SKIN_TONE: [CallbackQueryHandler(handle_skin_tone, pattern="^skin_")],
            HAIR_COLOR: [CallbackQueryHandler(handle_hair_color, pattern="^hair_")],
            FACE_SHAPE: [CallbackQueryHandler(handle_face_shape, pattern="^face_")],
            OCCASION: [CallbackQueryHandler(handle_occasion, pattern="^occasion_")],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

