from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# SQLite база данных будет создана в корне проекта
DB_PATH = Path(__file__).parent / "makeup_bot.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Highlighter(Base):
    __tablename__ = "highlighters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Lipstick(Base):
    __tablename__ = "lipsticks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class LipGloss(Base):
    __tablename__ = "lip_glosses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Foundation(Base):
    __tablename__ = "foundations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Eyeshadow(Base):
    __tablename__ = "eyeshadows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Mascara(Base):
    __tablename__ = "mascaras"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Blush(Base):
    __tablename__ = "blushes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


class Eyeliner(Base):
    __tablename__ = "eyeliners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(JSON, nullable=False)
    eye_color = Column(JSON, nullable=False)
    hair_color = Column(JSON, nullable=True)
    face_shape = Column(JSON, nullable=True)
    occasion = Column(JSON, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

