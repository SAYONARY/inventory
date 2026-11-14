"""Система учёта инвентаря компьютерных классов — консольное меню."""
from inventory import (STATES, TYPES, add_item, delete_item, filter_items,
                       find_by_number, find_by_room, format_item, update_item)
from storage import load_items, save_items

MENU = """
=== Учёт инвентаря ===
1. Показать оборудование
2. Добавить оборудование
3. Найти оборудование
4. Изменить запись
5. Удалить запись
0. Выход
"""


def _save(items):
    """Сохраняет данные в файл; при ошибке записи выводит сообщение."""
    try:
        save_items(items)
    except OSError as error:
        print("Не удалось сохранить данные:", error)


def show_items(items):
    if not items:
        print("Список пуст.")
        return
    for item in items:
        print(format_item(item))


def add_item_dialog(items):
    """Запрашивает данные у пользователя и добавляет запись."""
    inv_number = input("Инвентарный номер: ")
    print("Типы:", ", ".join(TYPES))
    item_type = input("Тип: ")
    name = input("Наименование: ")
    room = input("Кабинет: ")
    print("Состояния:", ", ".join(STATES))
    state = input("Состояние: ")
    try:
        item = add_item(items, inv_number, item_type, name, room, state)
    except ValueError as error:
        print("Ошибка:", error)
        return
    _save(items)
    print("Добавлено:", format_item(item))


def search_dialog(items):
    """Поиск по инвентарному номеру, по кабинету или по состоянию."""
    print("Искать: 1 - по инвентарному номеру, 2 - по кабинету, 3 - по состоянию")
    mode = input("Выберите: ").strip()
    if mode == "1":
        item = find_by_number(items, input("Инвентарный номер: "))
        if item is None:
            print("Не найдено.")
        else:
            print(format_item(item))
    elif mode == "2":
        found = find_by_room(items, input("Кабинет: "))
        if not found:
            print("Не найдено.")
        else:
            show_items(found)
    elif mode == "3":
        print("Состояния:", ", ".join(STATES))
        found = filter_items(items, state=input("Состояние: "))
        if not found:
            print("Не найдено.")
        else:
            show_items(found)
    else:
        print("Неверный выбор. Введите 1, 2 или 3.")


def edit_dialog(items):
    """Изменение состояния или кабинета записи."""
    inv_number = input("Инвентарный номер: ")
    item = find_by_number(items, inv_number)
    if item is None:
        print("Не найдено.")
        return
    print(format_item(item))
    print("Изменить: 1 - состояние, 2 - кабинет")
    mode = input("Выберите: ").strip()
    try:
        if mode == "1":
            print("Состояния:", ", ".join(STATES))
            update_item(items, inv_number, state=input("Новое состояние: "))
        elif mode == "2":
            update_item(items, inv_number, room=input("Новый кабинет: "))
        else:
            print("Неверный выбор. Введите 1 или 2.")
            return
    except ValueError as error:
        print("Ошибка:", error)
        return
    _save(items)
    print("Изменено:", format_item(item))


def delete_dialog(items):
    """Удаление записи с подтверждением."""
    inv_number = input("Инвентарный номер: ")
    item = find_by_number(items, inv_number)
    if item is None:
        print("Не найдено.")
        return
    print(format_item(item))
    answer = input("Удалить эту запись? (да/нет): ").strip().lower()
    removed = delete_item(items, inv_number, confirmed=answer in ("да", "д"))
    if removed is None:
        print("Удаление отменено.")
    else:
        _save(items)
        print("Удалено:", format_item(removed))


def main():
    items, warning = load_items()
    if warning:
        print(warning)
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            show_items(items)
        elif choice == "2":
            add_item_dialog(items)
        elif choice == "3":
            search_dialog(items)
        elif choice == "4":
            edit_dialog(items)
        elif choice == "5":
            delete_dialog(items)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню. Введите число от 0 до 5.")


if __name__ == "__main__":
    main()
