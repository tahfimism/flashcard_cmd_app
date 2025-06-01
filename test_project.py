import pytest
from datetime import date
from project import get_id, add_card, delete_card, update_stats, filter_by_tag

# Helper function to create a mock card
def sample_card():
    return {
        "id": get_id(),
        "hint": "sample hint",
        "description": "sample description",
        "times_shown": 0,
        "times_correct": 0,
        "accuracy": 0.0,
        "last_shown": date.today().isoformat(),
        "last_correct": None,
        "stage": "weak",
        "tags": ["test"]
    }

def test_add_card(monkeypatch):
    cards = []
    inputs = iter(["Test hint", "Test desc", "tag1, tag2", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_card(cards)
    assert len(cards) == 1
    card = cards[0]
    assert card["hint"] == "Test hint"
    assert card["description"] == "Test desc"
    assert "tag1" in card["tags"]
    assert "tag2" in card["tags"]

def test_delete_card(monkeypatch):
    card = sample_card()
    cards = [card]
    monkeypatch.setattr("builtins.input", lambda _: card["hint"])
    monkeypatch.setattr("project.re_ask", lambda: True)  # <-- fix here
    result = delete_card(cards)
    assert result is True
    assert len(cards) == 0

def test_filter_by_tag():
    cards = [sample_card(), sample_card()]
    cards[1]["tags"] = ["other"]
    filtered = filter_by_tag(cards, "test")
    assert len(filtered) == 1
    assert filtered[0]["tags"] == ["test"]

def test_update_stats():
    card = sample_card()
    update_stats(card, corrected=True)
    assert card["times_shown"] == 1
    assert card["times_correct"] == 1
    assert card["accuracy"] == pytest.approx(1.0)
    assert card["stage"] == "strong"

    update_stats(card, corrected=False)
    assert card["times_shown"] == 2
    assert card["times_correct"] == 1
    assert card["accuracy"] == pytest.approx(0.5)
    assert card["stage"] == "strong"

    update_stats(card, corrected=False)
    assert card["accuracy"] == pytest.approx(1/3)
    assert card["stage"] == "weak"
