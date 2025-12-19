"""
Этот файл загружает данные из JSON файлов (папка data/) в PostgreSQL.

Зачем это нужно:
- бот ищет продукты в базе данных (а не напрямую в json)
- поэтому сначала мы создаем таблицы и заполняем их данными

Как пользоваться (вручную):
python3 load_data.py

"""

import json
from pathlib import Path

"""
Импортируем всё, что нужно для работы с БД и моделями.

engine в этом файле вообще не используется напрямую, но я его импортировал,
потому что видел так в примерах. Можно было убрать.
"""
from database import (
    engine,
    SessionLocal,
    init_db,
    Highlighter,
    Lipstick,
    LipGloss,
    Foundation,
    Eyeshadow,
    Mascara,
    Blush,
    Eyeliner,
)


"""
Здесь мы связываем "тип продукта" (строка) и класс SQLAlchemy.
Например: "lipstick" -> Lipstick (таблица lipsticks).
"""
PRODUCT_MODELS = {
    "highlighter": Highlighter,
    "lipstick": Lipstick,
    "lip_gloss": LipGloss,
    "foundation": Foundation,
    "eyeshadow": Eyeshadow,
    "mascara": Mascara,
    "blush": Blush,
    "eyeliner": Eyeliner,
}


def load_json_data(file_path: str, product_type: str):
    """
    Загружает один JSON файл в базу.

    file_path: путь до файла типа data/lipstick.json
    product_type: строка, например "lipstick"
    """
    db = SessionLocal()

    try:
        model_class = PRODUCT_MODELS.get(product_type)
        if not model_class:
            print(f"Неизвестный тип продукта: {product_type}")
            return

        """
        Читаем JSON как список словарей.
        В каждом словаре должны быть ключи:
        name, brand, color, skin_tone, eye_color, occasion, price, description, image_url
        """
        with open(file_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        loaded_count = 0

        for product_data in products:
            """
            Простой способ не добавлять полностью одинаковые записи:
            смотрим, есть ли уже продукт с таким (name + brand).
            """
            existing = (
                db.query(model_class)
                .filter_by(name=product_data["name"], brand=product_data["brand"])
                .first()
            )

            if existing:
                print(f"Продукт {product_data['name']} уже существует, пропускаем")
                continue

            """
            Создаем объект модели. **product_data распаковывает словарь в параметры.
            То есть примерно то же самое, что:
            product = model_class(name=..., brand=..., color=..., ...)
            """
            product = model_class(**product_data)
            db.add(product)
            loaded_count += 1

        """
        commit сохраняет изменения в базе.
        """
        db.commit()
        print(f"✓ Загружено {loaded_count} продуктов типа '{product_type}' из {file_path}")

    except Exception as e:
        """
        Если в середине что-то упало (ошибка JSON, ошибка БД),
        то откатываем транзакцию, чтобы не было "полузаписанных" данных.
        """
        db.rollback()
        print(f"✗ Ошибка при загрузке {file_path}: {e}")
    finally:
        db.close()


def main():
    """
    Загружаем все файлы из папки data/.
    """
    print("Инициализация базы данных...")

    """
    init_db создает таблицы (если их нет).
    """
    init_db()
    print("✓ База данных инициализирована\n")

    """
    Находим папку data рядом с этим файлом.
    """
    data_dir = Path(__file__).parent / "data"

    """
    Файл -> тип продукта.
    """
    file_mapping = {
        "highlighter.json": "highlighter",
        "lipstick.json": "lipstick",
        "lip_gloss.json": "lip_gloss",
        "foundation.json": "foundation",
        "eyeshadow.json": "eyeshadow",
        "mascara.json": "mascara",
        "blush.json": "blush",
        "eyeliner.json": "eyeliner",
    }

    for filename, product_type in file_mapping.items():
        file_path = data_dir / filename
        if file_path.exists():
            print(f"Загрузка {filename}...")
            load_json_data(str(file_path), product_type)
        else:
            print(f"✗ Файл {filename} не найден")

    print("\n✓ Загрузка данных завершена!")


if __name__ == "__main__":
    main()

