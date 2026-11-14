import json
import os

from storage import load_items, save_items

SAMPLE = [
    {"inv_number": "INV-001", "type": "ПК", "name": "Dell OptiPlex 3080", "room": "101", "state": "исправно"},
    {"inv_number": "INV-002", "type": "монитор", "name": "Samsung S24", "room": "101", "state": "исправно"},
]


def test_load_missing_file_returns_empty(tmp_path):
    items, warning = load_items(str(tmp_path / "inventory.json"))
    assert items == []
    assert warning is None


def test_load_empty_file_returns_empty(tmp_path):
    path = tmp_path / "inventory.json"
    path.write_text("", encoding="utf-8")
    items, warning = load_items(str(path))
    assert items == []
    assert warning is None


def test_save_and_load_roundtrip(tmp_path):
    path = str(tmp_path / "inventory.json")
    save_items(SAMPLE, path)
    items, warning = load_items(path)
    assert items == SAMPLE
    assert warning is None


def test_save_creates_missing_folder(tmp_path):
    path = str(tmp_path / "data" / "inventory.json")
    save_items(SAMPLE, path)
    assert os.path.exists(path)


def test_save_keeps_cyrillic(tmp_path):
    path = tmp_path / "inventory.json"
    save_items(SAMPLE, str(path))
    assert "исправно" in path.read_text(encoding="utf-8")


def test_data_survives_restart(tmp_path):
    path = str(tmp_path / "inventory.json")
    items, _ = load_items(path)
    items.append(dict(SAMPLE[0]))
    save_items(items, path)
    reloaded, _ = load_items(path)
    reloaded[0]["state"] = "списано"
    save_items(reloaded, path)
    final, _ = load_items(path)
    assert len(final) == 1
    assert final[0]["state"] == "списано"


def test_broken_json_is_kept_as_backup(tmp_path):
    path = tmp_path / "inventory.json"
    path.write_text("{ не json", encoding="utf-8")
    items, warning = load_items(str(path))
    assert items == []
    assert warning is not None
    backup = tmp_path / "inventory.json.broken"
    assert backup.exists()
    assert backup.read_text(encoding="utf-8") == "{ не json"
    assert not path.exists()


def test_wrong_structure_is_kept_as_backup(tmp_path):
    path = tmp_path / "inventory.json"
    path.write_text(json.dumps({"inv_number": "INV-001"}), encoding="utf-8")
    items, warning = load_items(str(path))
    assert items == []
    assert warning is not None
    assert (tmp_path / "inventory.json.broken").exists()


def test_sample_file_has_at_least_10_valid_records():
    sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "data", "inventory.json")
    items, warning = load_items(sample_path)
    assert warning is None
    assert len(items) >= 10
    numbers = [item["inv_number"] for item in items]
    assert len(numbers) == len(set(numbers))
