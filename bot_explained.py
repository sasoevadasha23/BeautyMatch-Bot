"""
Файл bot_explained.py

Это такая же версия, как bot.py, только с подробными пояснениями.

Задача этого файла простая:
- создать Telegram-приложение (python-telegram-bot)
- подключить к нему обработчики (handlers) из handlers.py
- запустить бота через polling

ВАЖНО:
Обычно токен лучше хранить в .env (или хотя бы в переменных окружения).
Но тут токен просто строкой, потому что это учебный проект.
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

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


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


BOT_TOKEN = "8289291625:AAF1uUJWnknXZ7Yiy3896jWS0UkEmCW6MCQ"


def main():
    """
    Application — это главный объект python-telegram-bot.
    В него добавляются handler'ы (обработчики).

    Мы импортируем обработчики из handlers.py, чтобы bot.py был максимально простой.
    """
    # На всякий случай создаем таблицы/колонки в базе.
    # Это нужно, потому что в json теперь есть hair_color и face_shape, и в базе тоже должны быть такие колонки.
    init_db()

    # Создаем приложение бота.
    # В Application мы потом добавляем handlers.
    application = Application.builder().token(BOT_TOKEN).build()

    """
    ConversationHandler нужен, чтобы делать диалог по шагам.
    В нашем случае это 5 вопросов, и потом финальная рекомендация.
    """
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("quiz", quiz_start)],
        states={
            # Тут расписано: на каком шаге какие кнопки мы ожидаем.
            EYE_COLOR: [CallbackQueryHandler(handle_eye_color, pattern="^eye_")],
            SKIN_TONE: [CallbackQueryHandler(handle_skin_tone, pattern="^skin_")],
            HAIR_COLOR: [CallbackQueryHandler(handle_hair_color, pattern="^hair_")],
            FACE_SHAPE: [CallbackQueryHandler(handle_face_shape, pattern="^face_")],
            OCCASION: [CallbackQueryHandler(handle_occasion, pattern="^occasion_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Обычные команды.
    application.add_handler(CommandHandler("start", start))

    # Весь "опросник" (/quiz) идет одним ConversationHandler.
    application.add_handler(conv_handler)

    """
    allowed_updates=Update.ALL_TYPES — на всякий случай, чтобы бот получал все типы апдейтов.
    """
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

