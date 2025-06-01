import sys
import json
import csv
import uuid
from tabulate import tabulate
from datetime import date
from InquirerPy import prompt
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
console = Console()



options = ["Review Cards", "Review by tag", "Review by stage", "search", "show all cards", "Add Card", "Delete cards", "Filter", "Import Cards", "Export cards", "Exit"]
stages = ["weak", "strong"]



def main():

    # LOAD all cards from JSON file
    cards = load_cards("cards.json")


    # get user promt

    while True:
        print()
        promt = get_promt(options).lower()
        print(promt)

        match promt:
            case "exit":
                save_cards(cards)
                sys.exit("\nsee u next time \n\n")

            case "add card":
                add_card(cards)

            case "review cards":
                review_cards(cards, tag=None)

            case "delete cards":

                while True:
                    if delete_card(cards):
                        print("card is deleted")
                        save_cards(cards)
                    else:
                        print("card is not found")

                    ans = input('Press enter to delete another or type "n" or "no": ').strip().lower()
                    if ans in ["n", "no"]:
                        break


            case "show all cards":
                print_all(cards)

            case "filter":
                filter = input("filter: ").strip().lower()
                filter_print(cards, filter)

            case "review by stage" :
                ans = get_promt(stages)
                review_cards(cards, tag=ans)

            case "review by tag" :
                tags = get_tags(cards)
                ans = get_promt(tags)
                review_cards(cards, tag=ans)

            case "import cards":
                import_cards(cards)

            case "export cards":
                export_cards(cards, "exported_cards_nn.csv")

            case "search":
                query = input("Search for: ").strip().lower()
                matches = search_cards(cards, query)
                if matches:
                    print_all(matches)
                else:
                    print("No results found.")






def print_card(card, type=0):

    """Render a single flashcard using rich.Panel.

    Args:
        card (dict): The flashcard to display.
        type (int): 0 for hint/front side, 1 for answer/back side.

    Side Effects:
        - Renders card in the terminal using color and formatting.
    """

    if type == 1:
        text = card["description"]
        colour_text = "light_sky_blue1"
        colour_title = "sky_blue1"
        header = "Answer"
    else:
        text = card["hint"]
        colour_text = "bold bright_magenta"
        colour_title = "magenta"
        header = "FLASHCARD"


    panel_content = f"[bold cyan]{text}[/bold cyan]\n\n"
    panel = Panel(
        Align.center(panel_content, vertical="middle"),
        title= header,
        width=60,
        padding=(2, 4),
        border_style= colour_title,
    )
    console.print(panel)







def print_all(cards):

    """Display all flashcards in a formatted table sorted by accuracy.

    Args:
        cards (list): List of card dictionaries.

    Side Effects:
        - Prints total card count and formatted table.
    """

    header = [["hint", "description", "accuracy", "strength", "tags"],]
    card_list = []

    for card in cards:
        card_list.append([card["hint"], card["description"], card["accuracy"], card["stage"], card["tags"]])

    # print summary
    print()
    print(f"total number of cards: {len(cards)}")


    # sorting by accuracy
    card_list.sort(key=lambda x: x[2])  # x[2] = accuracy column

    # print all cards in table
    print(tabulate(header + card_list, tablefmt="grid"))







def filter_print(cards, filter_tag):

    """Display cards filtered by stage (weak/strong) or specific tag.

    Args:
        cards (list): List of flashcard dictionaries.
        filter_tag (str): Tag or stage to filter by.

    Side Effects:
        - Prints filtered card list or message if none found.
    """

    header = [["hint", "description", "accuracy", "tags"],]
    card_list = []
    if filter_tag in ["strong", "weak"]:

        for card in cards:
            if card["stage"] == filter_tag:
                card_list.append([
                    card["hint"], card["description"], card["accuracy"], card["tags"]
                ])


    else:

        for card in cards:
            if filter_tag in card.get("tags", []):
                card_list.append([
                    card["hint"], card["description"], card["accuracy"], card["tags"]
                ])

    # sorting by accuracy
    card_list.sort(key=lambda x: x[2])  # x[2] = accuracy column

    if len(card_list) == 0:
        print(f"[!] No cards found for '{filter_tag}'")
    else:
        print()
        print(f"cards dound: {len(card_list)}")
        print(tabulate(header + card_list, headers="firstrow", tablefmt="grid"))






def filter_by_tag(cards, tag):
    """Filter cards containing a specific tag.

    Args:
        cards (list): List of card dictionaries.
        tag (str): Tag to filter by.

    Returns:
        list: Filtered list of cards.
    """
    return [card for card in cards if tag in card.get("tags", [])]


def filter_by_stage(cards, stage):

    """Filter cards by their strength stage (e.g., weak or strong).

    Args:
        cards (list): List of card dictionaries.
        stage (str): The stage to filter by.

    Returns:
        list: Filtered list of cards.
    """

    return [card for card in cards if stage in card["stage"]]


def get_tags(cards):

    """Get a unique list of all tags used across cards.

    Args:
        cards (list): List of card dictionaries.

    Returns:
        list: Unique list of tags.
    """

    tags = []
    for card in cards:
        card_tags = card.get("tags", [])
        tags.extend(card_tags)
    return list(set(tags))



def load_cards(filename):
    """Load flashcards from a JSON file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        list: List of flashcard dictionaries.

    Side Effects:
        - If file doesn't exist, creates an empty JSON file and exits.
        - If JSON is invalid, returns empty list.
    """

    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        with open(filename, "w") as f:
            json.dump([], f)
        sys.exit("file didnt exist, now created, run the proram again")
    except json.JSONDecodeError:
        print("Error loading JSON. Starting with empty deck.")
        return []






def save_cards(cards, filename="cards.json"):

    """Save the current flashcards list to a JSON file.

    Args:
        cards (list): List of card dictionaries.
        filename (str): Target filename (default: cards.json).

    Side Effects:
        - Writes card data to disk.
        - Prints success or error message.
    """

    try:
        with open(filename, "w") as f:
            json.dump(cards, f, indent=4)
        print(f"[INFO] Cards saved to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save cards: {e}")




def import_cards(cards):

    """Import flashcards from a CSV file.

    Args:
        cards (list): The current list of cards to append to.
        filename (str): Path to CSV file.

    Side Effects:
        - Reads cards from CSV and adds them to the deck.
        - Saves updated list to JSON.
        - Skips malformed rows.
    """

    # print rules to write csv
    print("FORMAT: ur csv file have to be in the following format")
    print("card hint, description, tag1, tag2, ....")
    print("Recommended to use quotation around \"description\", tags are optional")
    print()

    while True:
        try:
            filename = input("Name of the file u want to import from (filename.csv): ")
            count = 0
            with open(filename, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 2:
                        continue  # Skip invalid rows

                    card = {
                        "id": get_id(),
                        "hint": row[0].strip(),
                        "description": row[1].strip(),
                        "times_shown": 0,
                        "times_correct": 0,
                        "accuracy": 0.0,
                        "last_shown": date.today().isoformat(),
                        "last_correct": None,
                        "stage": "weak",
                        "tags": [tag.strip().lower() for tag in row[2:]]
                    }
                    cards.append(card)
                    count += 1

            save_cards(cards)
            print(f"[INFO] {count} cards Imported from {filename}")
            break

        except FileNotFoundError:
            print(f"[ERROR] File not found: {filename}")
            pass
        except Exception as e:
            print(f"[ERROR] Failed to import cards: {e}")
            pass





def export_cards(cards, filename):

    """Export flashcards to a CSV file.

    Each row will contain the card's hint, description, and all associated tags.

    Args:
        cards (list): List of card dictionaries to export.
        filename (str): Destination CSV filename.

    Side Effects:
        - Writes flashcard data to a CSV file.
        - Prints confirmation message on success.
    """

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for card in cards:
            writer.writerow([card["hint"], card["description"]] + card["tags"])
    print(f"Exported {len(cards)} cards to {filename}")



def search_cards(cards, query):

    """Search flashcards by a keyword in hint or description.

    Args:
        cards (list): List of card dictionaries to search in.
        query (str): Search keyword (case-insensitive).

    Returns:
        list: Cards where the query matches hint or description.
    """

    query = query.lower()
    return [
        card for card in cards
        if query in card["hint"].lower() or query in card["description"].lower()
    ]




def review_cards(cards, tag=None):

    """Run a review session for flashcards, filtered optionally by tag or stage.

    Args:
        cards (list): List of all flashcards.
        tag (str or None): Tag or stage to filter by before review.

    Side Effects:
        - Displays each card.
        - Prompts user to self-assess correctness.
        - Updates card statistics.
    """
    # Show cards one-by-one (maybe shuffled)
    # Allow skip, mark correct/incorrect

    if tag in ["strong", "weak"]:
        cards = filter_by_stage(cards, tag)
    elif tag:
        cards = filter_by_tag(cards, tag)

    print(f"{len(cards)} Cards to review. Press enter to review")
    # loop thru cards
    for card in cards:

        # print card
        print_card(card)

        print(f"Stage: {card['stage']}, corrected last time: {'yes' if card['last_correct'] else 'no'}")

        # press enter to see other side
        input("u can write ur thoughts here, press enter to see the other side \n")

        # print other side
        print_card(card, 1)


        # update status
        corrected = get_correct()
        update_stats(card, corrected)


        # press enter to see next card
        next = input("press enter to see next card or type exit to stop reviewing: \n")
        if next == "exit":
            break
    print()
    print("you reviewed all the cards")








def get_correct():

    """Ask the user if they got the card correct.

    Returns:
        bool: True if user says they got it correct, False otherwise.
    """

    while True:
        ans = input("Did you get it correct? (y/n): ").strip().lower()
        if ans in ["y", "yes"]:
            return True
        elif ans in ["n", "no"]:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")








def update_stats(card, corrected=True):

    """Update statistics of a card after reviewing it.

    Args:
        card (dict): The card to update.
        corrected (bool): Whether the user got it correct.

    Side Effects:
        - Updates times shown, times correct, accuracy, last shown, and stage.
    """

    # Increment shown
    card["times_shown"] += 1

    # If correct, increment correct
    if corrected == True:
        card["times_correct"] += 1
        card["last_correct"] = date.today().isoformat()


    # Update accuracy and last_shown date
    card["accuracy"] = (
        card["times_correct"] / card["times_shown"] if card["times_shown"] else 0 )
    card["last_shown"] = date.today().isoformat()

    # update stage
    card["stage"] = "weak" if card["accuracy"] < 0.5 else "strong"



def get_promt(choices):

    """Prompt the user with a list of choices using InquirerPy.

    Args:
        choices (list): List of string options.

    Returns:
        str: The selected choice.
    """

    questions = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "choices": choices,
            "name": "action"
        }
    ]

    answer = prompt(questions)
    return answer["action"]





def re_ask():

    """Prompt the user for confirmation (yes or no).

    Returns:
        bool: True if user confirmed with 'y', False if 'n'.
    """

    ans = input("Are you sure? (y/n): ").strip().lower()
    if ans == "y":
        return True
    elif ans == "n":
        return False
    else:
        print("Invalid input.")
        return re_ask()  # Ask again if invalid input





def get_id():
    """Generate a unique string-based ID using UUID4.

    Returns:
        str: A unique identifier string.
    """
    return str(uuid.uuid4())


def add_card(cards):

    """Add new flashcards interactively.

    Args:
        cards (list): The current list of cards to append to.

    Side Effects:
        - Prompts user for hint, description, and optional tags.
        - Appends new cards to `cards`.
        - Saves updated card list to JSON file.
    """

    while True:
        hint = input("Card hint/title:  ")
        desc = input("Other side of card/description:  ")

        if not hint.strip():
            print("Hint cannot be empty.")
            continue

        if any(c["hint"].lower() == hint.lower() for c in cards):
            print("A card with this hint already exists. Skipping...")
            continue

        # Get tags input from user
        tags_input = input("Enter tags (comma-separated): ").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()] if tags_input else []

        card = {
            "id": get_id(),
            "hint": hint,
            "description": desc,
            "times_shown": 0,
            "times_correct": 0,
            "accuracy": 0.0,
            "last_shown": date.today().isoformat(),
            "last_correct": None,
            "stage": "weak",
            "tags": tags
        }

        cards.append(card)

        ans = input('Press enter to add another or type "n" or "no": ').strip().lower()
        if ans in ["n", "no"]:
            break

    save_cards(cards)




def delete_card(cards):

    """Delete a flashcard by hint or ID after confirmation.

    Args:
        cards (list): List of card dictionaries.

    Returns:
        bool: True if a card was deleted, False otherwise.
    """

    hint = input("Enter card's hint or id: ").strip().lower()

    for card in cards:
        # Check by hint or ID
        if card["hint"].lower() == hint or card["id"] == hint:
            if re_ask():
                cards.remove(card)
                return True
            else:
                return False
    return False  # Only return False if loop finishes without deleting






main()
