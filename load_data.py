import json
from pathlib import Path
from database import (
    engine, SessionLocal, init_db,
    Highlighter, Lipstick, LipGloss, Foundation, Eyeshadow, Mascara, Blush, Eyeliner
)

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
    db = SessionLocal()
    
    try:
        model_class = PRODUCT_MODELS.get(product_type)
        if not model_class:
            print(f"Неизвестный тип продукта: {product_type}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        loaded_count = 0
        for product_data in products:
            existing = db.query(model_class).filter_by(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if existing:
                changed = False
                for k in ["hair_color", "face_shape"]:
                    if k in product_data:
                        if getattr(existing, k, None) != product_data[k]:
                            setattr(existing, k, product_data[k])
                            changed = True

                if changed:
                    loaded_count += 1
                else:
                    print(f"Продукт {product_data['name']} уже существует, пропускаем")
                continue
            
            product = model_class(**product_data)
            db.add(product)
            loaded_count += 1
        
        db.commit()
        print(f"✓ Загружено {loaded_count} продуктов типа '{product_type}' из {file_path}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Ошибка при загрузке {file_path}: {e}")
    finally:
        db.close()


def main():
    print("Инициализация базы данных...")
    init_db()
    print("✓ База данных инициализирована\n")
    
    data_dir = Path(__file__).parent / "data"
    
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

