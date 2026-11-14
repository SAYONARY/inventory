"""Хранение записей в JSON-файле data/inventory.json."""
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "inventory.json")
REQUIRED_KEYS = ("inv_number", "type", "name", "room", "state")


def _is_valid(data):
    """Проверяет структуру данных: список записей, у каждой есть все поля со строковыми значениями."""
    if not isinstance(data, list):
        return False
    for item in data:
        if not isinstance(item, dict):
            return False
        for key in REQUIRED_KEYS:
            if not isinstance(item.get(key), str):
                return False
    return True


def _backup_broken(path):
    """Переносит повреждённый файл в копию рядом, чтобы данные не пропали незаметно."""
    backup = path + ".broken"
    if os.path.exists(backup):
        backup = f"{path}.broken-{datetime.now():%Y%m%d-%H%M%S}"
    os.replace(path, backup)
    return backup


def load_items(path=DATA_FILE):
    """Загружает записи из файла. Возвращает пару (записи, предупреждение).

    Нет файла или он пустой — пустой список без предупреждения.
    Файл повреждён — он переименовывается в копию .broken, возвращается пустой список
    и предупреждение.
    """
    if not os.path.exists(path):
        return [], None
    try:
        with open(path, encoding="utf-8") as file:
            text = file.read()
        if not text.strip():
            return [], None
        data = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        data = None
    if not _is_valid(data):
        backup = _backup_broken(path)
        return [], (f"Файл данных повреждён. Он сохранён как {backup}, "
                    "программа начинает с пустого списка.")
    return data, None


def save_items(items, path=DATA_FILE):
    """Сохраняет записи в файл (сначала во временный файл, затем замена основного)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)
    os.replace(temp_path, path)
