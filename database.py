from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import getpass

current_user = getpass.getuser()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://{current_user}@localhost:5432/makeup_bot"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Highlighter(Base):
    __tablename__ = "highlighters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skin_tone = Column(ARRAY(String), nullable=False)
    eye_color = Column(ARRAY(String), nullable=False)
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
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
    hair_color = Column(ARRAY(String), nullable=True)
    face_shape = Column(ARRAY(String), nullable=True)
    occasion = Column(ARRAY(String), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    image_url = Column(String)


def _ensure_extra_columns():
    tables = [
        "highlighters",
        "lipsticks",
        "lip_glosses",
        "foundations",
        "eyeshadows",
        "mascaras",
        "blushes",
        "eyeliners",
    ]

    with engine.begin() as conn:
        for t in tables:
            conn.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS hair_color VARCHAR[]"))
            conn.execute(text(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS face_shape VARCHAR[]"))

            col_type = conn.execute(
                text(
                    "SELECT udt_name FROM information_schema.columns "
                    "WHERE table_name = :t AND column_name = :c"
                ),
                {"t": t, "c": "hair_color"},
            ).scalar()
            if col_type == "_text":
                conn.execute(
                    text(f"ALTER TABLE {t} ALTER COLUMN hair_color TYPE VARCHAR[] USING hair_color::varchar[]")
                )

            col_type = conn.execute(
                text(
                    "SELECT udt_name FROM information_schema.columns "
                    "WHERE table_name = :t AND column_name = :c"
                ),
                {"t": t, "c": "face_shape"},
            ).scalar()
            if col_type == "_text":
                conn.execute(
                    text(f"ALTER TABLE {t} ALTER COLUMN face_shape TYPE VARCHAR[] USING face_shape::varchar[]")
                )


def init_db():
    Base.metadata.create_all(bind=engine)
    _ensure_extra_columns()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

