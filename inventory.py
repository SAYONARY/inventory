"""Модель записи об оборудовании и операции с ней (без ввода-вывода)."""

TYPES = ("ПК", "монитор", "принтер", "проектор", "другое")
STATES = ("исправно", "требует ремонта", "списано")

FIELD_TITLES = {
    "inv_number": "Инвентарный номер",
    "type": "Тип",
    "name": "Наименование",
    "room": "Кабинет",
    "state": "Состояние",
}

DEMO_ITEMS = [
    {"inv_number": "INV-001", "type": "ПК", "name": "Dell OptiPlex 3080", "room": "101", "state": "исправно"},
    {"inv_number": "INV-002", "type": "монитор", "name": "Samsung S24", "room": "101", "state": "исправно"},
    {"inv_number": "INV-003", "type": "принтер", "name": "HP LaserJet 1018", "room": "205", "state": "требует ремонта"},
    {"inv_number": "INV-004", "type": "ПК", "name": "Lenovo ThinkCentre M70", "room": "102", "state": "исправно"},
    {"inv_number": "INV-005", "type": "проектор", "name": "Epson EB-X06", "room": "301", "state": "списано"},
    {"inv_number": "INV-006", "type": "монитор", "name": "LG 22MK430", "room": "102", "state": "исправно"},
]


def get_items():
    """Возвращает независимые копии демонстрационных записей."""
    return [dict(item) for item in DEMO_ITEMS]


def format_item(item):
    """Строка с карточкой одной записи."""
    return (f"{item['inv_number']} | {item['type']} | {item['name']} | "
            f"каб. {item['room']} | {item['state']}")


def _norm(value):
    """Строка для сравнения: без пробелов по краям и без учёта регистра."""
    return value.strip().casefold()


def _not_found_message(inv_number):
    return f"Не найдено: записи с номером {inv_number.strip()} нет."


def _check_choice(value, allowed, message_start):
    """Проверяет, что значение входит в список допустимых."""
    if value.strip() not in allowed:
        raise ValueError(f"{message_start}: " + ", ".join(allowed) + ".")


def find_by_number(items, inv_number):
    """Ищет запись по инвентарному номеру. Возвращает запись или None."""
    wanted = _norm(inv_number)
    if not wanted:
        return None
    for item in items:
        if _norm(item["inv_number"]) == wanted:
            return item
    return None


def number_exists(items, inv_number):
    """Проверяет, есть ли в списке запись с таким инвентарным номером."""
    return find_by_number(items, inv_number) is not None


def filter_items(items, room=None, state=None):
    """Отбирает записи по кабинету и/или состоянию. Без условий возвращает все записи."""
    result = list(items)
    if room is not None:
        result = [item for item in result if _norm(item["room"]) == _norm(room)]
    if state is not None:
        result = [item for item in result if _norm(item["state"]) == _norm(state)]
    return result


def find_by_room(items, room):
    """Возвращает записи из указанного кабинета (пустой список, если нет или ввод пустой)."""
    if not room.strip():
        return []
    return filter_items(items, room=room)


def validate_item(items, inv_number, item_type, name, room, state):
    """Проверяет данные новой записи. При ошибке вызывает ValueError."""
    values = (inv_number, item_type, name, room, state)
    for key, value in zip(FIELD_TITLES, values):
        if not value or not value.strip():
            raise ValueError(f"Поле «{FIELD_TITLES[key]}» не может быть пустым.")
    _check_choice(item_type, TYPES, "Тип должен быть одним из")
    _check_choice(state, STATES, "Состояние должно быть одним из")
    if number_exists(items, inv_number):
        raise ValueError(f"Запись с номером {inv_number.strip()} уже существует.")


def add_item(items, inv_number, item_type, name, room, state):
    """Добавляет запись в список и возвращает её. При ошибке данных — ValueError."""
    validate_item(items, inv_number, item_type, name, room, state)
    item = {
        "inv_number": inv_number.strip(),
        "type": item_type.strip(),
        "name": name.strip(),
        "room": room.strip(),
        "state": state.strip(),
    }
    items.append(item)
    return item


def update_item(items, inv_number, room=None, state=None):
    """Меняет кабинет и/или состояние записи. При ошибке — ValueError."""
    item = find_by_number(items, inv_number)
    if item is None:
        raise ValueError(_not_found_message(inv_number))
    if room is None and state is None:
        raise ValueError("Нечего изменять: укажите кабинет или состояние.")
    if room is not None and not room.strip():
        raise ValueError("Кабинет не может быть пустым.")
    if state is not None:
        _check_choice(state, STATES, "Состояние должно быть одним из")
    if room is not None:
        item["room"] = room.strip()
    if state is not None:
        item["state"] = state.strip()
    return item


def delete_item(items, inv_number, confirmed=False):
    """Удаляет запись только при confirmed=True. Если подтверждения нет, запись остаётся
    и возвращается None. Если записи нет — ValueError."""
    item = find_by_number(items, inv_number)
    if item is None:
        raise ValueError(_not_found_message(inv_number))
    if not confirmed:
        return None
    items.remove(item)
    return item
