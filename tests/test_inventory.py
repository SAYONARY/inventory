import pytest

from inventory import (add_item, delete_item, filter_items, find_by_number,
                       find_by_room, get_items, update_item)


# --- Спринт 2: добавление ---

def test_add_item_success():
    items = get_items()
    count = len(items)
    item = add_item(items, "INV-100", "ПК", "HP ProDesk", "110", "исправно")
    assert len(items) == count + 1
    assert item["inv_number"] == "INV-100"


@pytest.mark.parametrize("field_index", range(5))
def test_add_item_empty_field(field_index):
    items = get_items()
    values = ["INV-101", "ПК", "HP ProDesk", "110", "исправно"]
    values[field_index] = "   "
    count = len(items)
    with pytest.raises(ValueError):
        add_item(items, *values)
    assert len(items) == count


def test_add_item_duplicate_number():
    items = get_items()
    count = len(items)
    with pytest.raises(ValueError):
        add_item(items, "INV-001", "ПК", "Другой ПК", "110", "исправно")
    assert len(items) == count


# --- Спринт 3: поиск ---

def test_find_by_number_existing():
    items = get_items()
    item = find_by_number(items, "INV-003")
    assert item is not None
    assert item["name"] == "HP LaserJet 1018"


def test_find_by_number_missing():
    assert find_by_number(get_items(), "INV-999") is None


def test_find_by_number_empty_input():
    assert find_by_number(get_items(), "   ") is None


def test_find_by_number_repeat_search():
    items = get_items()
    assert find_by_number(items, "INV-002") == find_by_number(items, "INV-002")


def test_find_by_room_existing():
    found = find_by_room(get_items(), "101")
    assert [item["inv_number"] for item in found] == ["INV-001", "INV-002"]


def test_find_by_room_missing():
    assert find_by_room(get_items(), "999") == []


# --- Спринт 3: изменение ---

def test_update_state():
    items = get_items()
    item = update_item(items, "INV-001", state="требует ремонта")
    assert item["state"] == "требует ремонта"
    assert find_by_number(items, "INV-001")["state"] == "требует ремонта"


def test_update_room():
    items = get_items()
    update_item(items, "INV-001", room="305")
    assert find_by_number(items, "INV-001")["room"] == "305"


def test_update_missing_number():
    with pytest.raises(ValueError):
        update_item(get_items(), "INV-999", state="исправно")


def test_update_invalid_state():
    items = get_items()
    with pytest.raises(ValueError):
        update_item(items, "INV-001", state="сломано")
    assert find_by_number(items, "INV-001")["state"] == "исправно"


# --- Спринт 3: удаление ---

def test_delete_confirmed():
    items = get_items()
    count = len(items)
    removed = delete_item(items, "INV-006", confirmed=True)
    assert removed["inv_number"] == "INV-006"
    assert len(items) == count - 1
    assert find_by_number(items, "INV-006") is None


def test_delete_cancelled():
    items = get_items()
    count = len(items)
    assert delete_item(items, "INV-006", confirmed=False) is None
    assert len(items) == count


def test_delete_missing_number():
    with pytest.raises(ValueError):
        delete_item(get_items(), "INV-999", confirmed=True)


# --- Спринт 5: регрессия и дополнительные проверки ---

def test_get_items_returns_independent_copies():
    first = get_items()
    first[0]["state"] = "списано"
    assert get_items()[0]["state"] == "исправно"


def test_add_item_trims_spaces():
    items = get_items()
    item = add_item(items, "  INV-110  ", " ПК ", "  HP ProDesk  ", " 110 ", " исправно ")
    assert item == {"inv_number": "INV-110", "type": "ПК", "name": "HP ProDesk",
                    "room": "110", "state": "исправно"}


def test_add_item_invalid_type():
    items = get_items()
    with pytest.raises(ValueError):
        add_item(items, "INV-111", "frf", "HP ProDesk", "110", "исправно")
    assert len(items) == 6


def test_add_item_invalid_state():
    items = get_items()
    with pytest.raises(ValueError):
        add_item(items, "INV-112", "ПК", "HP ProDesk", "110", "df")
    assert len(items) == 6


def test_add_item_duplicate_ignores_case_and_spaces():
    items = get_items()
    with pytest.raises(ValueError):
        add_item(items, " inv-001 ", "ПК", "Другой ПК", "110", "исправно")


def test_find_by_room_empty_input():
    assert find_by_room(get_items(), "   ") == []


def test_find_by_number_ignores_case_and_spaces():
    assert find_by_number(get_items(), "  inv-003 ")["inv_number"] == "INV-003"


def test_update_empty_room():
    items = get_items()
    with pytest.raises(ValueError):
        update_item(items, "INV-001", room="   ")
    assert find_by_number(items, "INV-001")["room"] == "101"


def test_update_nothing_to_change():
    with pytest.raises(ValueError):
        update_item(get_items(), "INV-001")


def test_filter_by_state():
    found = filter_items(get_items(), state="списано")
    assert [item["inv_number"] for item in found] == ["INV-005"]


def test_filter_by_room_and_state():
    found = filter_items(get_items(), room="102", state="исправно")
    assert [item["inv_number"] for item in found] == ["INV-004", "INV-006"]


def test_filter_no_match():
    assert filter_items(get_items(), state="требует ремонта", room="101") == []


def test_filter_without_conditions_returns_all():
    items = get_items()
    assert filter_items(items) == items


def test_filter_ignores_case_and_spaces():
    found = filter_items(get_items(), state="  ИСПРАВНО ")
    assert len(found) == 4
