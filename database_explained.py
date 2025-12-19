"""
В этом файле описаны модели базы данных (SQLAlchemy) и подключение к PostgreSQL.

Я сделал объясняющую версию, чтобы можно было читать и понимать,
а основной database.py оставил без комментариев.

Что здесь есть:
- DATABASE_URL (строка подключения)
- engine (движок)
- SessionLocal (создает сессии)
- Base (база для моделей)
- классы моделей (таблицы): Highlighter, Lipstick, ...
- init_db() чтобы создать таблицы
"""

import os
import getpass

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Я беру пользователя системы и делаю подключение к Postgres как:
# postgresql://<username>@localhost:5432/makeup_bot
# На macOS часто это работает без пароля (если локально), но не всегда.
current_user = getpass.getuser()

# Если есть переменная окружения DATABASE_URL, то используем её.
# Иначе используем вариант с текущим пользователем.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{current_user}@localhost:5432/makeup_bot",
)


# engine — это то, через что SQLAlchemy общается с базой.
engine = create_engine(DATABASE_URL)

# SessionLocal — "фабрика" для создания сессий.
# Сессия — это объект, через который мы делаем запросы и добавляем записи.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base нужен, чтобы описывать модели как классы.
Base = declarative_base()


"""
Дальше идут модели. Каждая модель = таблица.
__tablename__ — имя таблицы в базе.
Column(...) — это колонка.
ARRAY(String) — массив строк в Postgres, удобно хранить варианты (skin_tone и т.д.)
"""


class Highlighter(Base):
    __tablename__ = "highlighters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Lipstick(Base):
    __tablename__ = "lipsticks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class LipGloss(Base):
    __tablename__ = "lip_glosses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Foundation(Base):
    __tablename__ = "foundations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Eyeshadow(Base):
    __tablename__ = "eyeshadows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Mascara(Base):
    __tablename__ = "mascaras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Blush(Base):
    __tablename__ = "blushes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Eyeliner(Base):
    __tablename__ = "eyeliners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


def init_db():
    """
    create_all создаёт таблицы по всем моделям, которые наследуются от Base.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Это генератор, который возвращает сессию.
    Такой стиль обычно используют во фреймворках (типа FastAPI),
    но тут просто оставил, вдруг потом пригодится.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

