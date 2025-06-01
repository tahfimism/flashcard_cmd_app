# Flashcard Terminal App

#### Video Demo: [https://youtu.be/-CodZ0vJs6E?si=JRJcZpUix8uJJw_K](https://youtu.be/-CodZ0vJs6E?si=JRJcZpUix8uJJw_K)
#### Author: Nakib Noor
#### GitHub: tahfimism
#### edX Username: tahfimism
#### Location: Dhaka, ?Bangladesh
#### Date: June 1, 2025

---

### Description

This is a command-line based **Flashcard Learning Application** built in Python as my final project for CS50P. It allows users to create, store, review, and track flashcards in the terminal — no GUI required. The app is designed to simulate a  repetition system (SRS) with basic stats and filtering to help users identify weak areas and focus their practice.

This project was built from scratch using pure Python and some pip-installed libraries for improved terminal interactivity and aesthetics. It follows the final project specification strictly — with modular design, testable functions, and structured layout.

---

### Features

- 📇 **Add Flashcards** with hint, description, and tags
- 🗑️ **Delete Flashcards** by hint (with confirmation)
- 📊 **Track Statistics**: times shown, times correct, accuracy, last shown, last correct, stage (weak/strong)
- 🔍 **Filter by Tags** to focus on specific topics
- ✅ **Auto-updating Performance Metrics** based on answers
- 🎨 **Enhanced Terminal UI** using `rich`, `InquirerPy`, and `tabulate`
- 📁 **JSON Storage** for persistence across sessions
- 🧪 **Pytest-based Unit Tests** for core logic

---

### Project Structure

project/
├── project.py          # Main CLI logic and all functions
├── test_project.py     # Unit tests for core functions
├── requirements.txt    # List of required pip libraries
├── cards.json          # (Auto-generated) Flashcard database
└── README.md           # This file

---

### Files and Functions

#### `project.py`
- `main()`
  The entry point. Provides a CLI menu using `InquirerPy`.

- `add_card(cards)`
  Prompts user for flashcard details and adds to list.

- `delete_card(cards)`
  Deletes a flashcard by hint with optional confirmation via `re_ask()`.

- `update_stats(card, corrected)`
  Updates a card's statistics (times shown, accuracy, stage).

- `filter_by_tag(cards, tag)`
  Returns a filtered list of cards matching the given tag.

- Other helper functions:
  - `get_id()`: generates unique ID
  - `save_cards()` and `load_cards()`: handles JSON storage
  - `print_card()`: display the card in terminal

#### `test_project.py`
- `test_add_card()`: Tests if flashcard is added correctly with tags.
- `test_delete_card()`: Tests deletion logic with mocked confirmation.
- `test_update_stats()`: Tests accuracy/stage update logic for correct/incorrect answers.
- `test_filter_by_tag()`: Checks tag-based filtering behavior.



#### `requirements.txt`
Includes:
- `rich`
- `InquirerPy`
- `tabulate`
- (pytest not included here but assumed for dev)

---

### Design Considerations

- **Why CLI?**
  I wanted to avoid over-engineering and instead focused on a fast, usable CLI app. It is lightweight and runs on any terminal.

- **Why JSON instead of SQL?**
  Since the project is local and single-user, using a flat file was sufficient. It also reduced overhead and kept the project beginner-friendly.

- **Why not classes?**
  I opted for dictionary-based cards and procedural functions to keep the code more aligned with CS50P’s core teachings. However, the code is modular enough to refactor into OOP later.

- **Stage logic (weak vs. strong):**
  If a card’s accuracy falls below 50%, it’s considered weak. This helps in identifying which flashcards need more attention during review.

---

### Challenges

- Getting clean CLI interaction without GUI
- Designing testable logic while keeping I/O separate
- Ensuring the `update_stats()` function worked correctly for varying edge cases
- Mocking user input in tests using `monkeypatch`

---

### Future Improvements

- Put the functions in different files in some catagory
- Add a sumary feature
- Add spaced repetition scheduling (like Anki)
- Support for categories or decks
- Make a TUI version using `Textual` or `urwid`

---

### Final Notes

This project pushed me to think critically about design, testing, and user interaction in a command-line environment. It helped me strengthen my Python fundamentals while also introducing me to testing best practices. I’m proud of how much I built from scratch with a practical use-case in mind.

Thank you to the CS50 team for an amazing course!



