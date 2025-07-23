from io import TextIOWrapper as File
from json import load as json_to_dict
from typing import Any, Callable
from random import randint as lib_randint

cards_file: File = open("reference/cards.json", "r")
ALL_CARDS: list[dict[str, Any]] = json_to_dict(cards_file)["cards"]
cards_file.close()

supers_file: File = open("reference/superpowers.json", "r")
ALL_SUPERPOWERS: dict[str, list[str]] = json_to_dict(supers_file)["superpowers"]
supers_file.close()

# --------------------------------------------------------------------

def initialize_deck(lines: list[str]) -> list[str]:
    deck: list[str] = []
    for line in lines:
        count: int = int(line[-1])
        card: str = line[:-2]
        deck += count * [card]
    return deck

deck_file: File = open("input/deck.txt", "r")
deck_lines: list[str] = deck_file.read().split("\n")
DECK: list[str] = initialize_deck(deck_lines[1:])
SUPERPOWERS: list[str] = ALL_SUPERPOWERS[deck_lines[0]]
deck_file.close()

# --------------------------------------------------------------------

def random_index(l: list[Any]) -> int:
    return lib_randint(0, len(l) - 1)

# --------------------------------------------------------------------

def draw(args: list[str]) -> str:
    count: int = 1 if len(args) == 0 else int(args[0])
    result: list[str] = []
    for i in range(count):
        ri: int = random_index(DECK)
        card: str = DECK[ri]
        del DECK[ri]
        result.append(card)
    return ", ".join(result)

def ping(args: list[str]) -> str:
    return str(lib_randint(1, 3))

def block(args: list[str]) -> str:
    ri: int = random_index(SUPERPOWERS)
    superpower: str = SUPERPOWERS[ri]
    del SUPERPOWERS[ri]
    return superpower

def shuffle(args: list[str]) -> str:
    global DECK
    card: str = " ".join(args[:-1])
    count: int = int(args[-1])
    DECK += count * [card]
    copy_word: str = "copy" if count == 1 else "copies"
    return f"{count} {copy_word} of {card} has been shuffled into the deck."

def randint(args: list[str]) -> str:
    max: int = int(args[0])
    return str(lib_randint(1, max))

def test_deck(args: list[str]) -> str:
    return f"{len(DECK)}: {DECK}\n\n{len(SUPERPOWERS)}: {SUPERPOWERS}"

# --------------------------------------------------------------------

def start() -> None:
    raise NotImplementedError

# --------------------------------------------------------------------

def conjure(args: list[str]) -> str:
    raise NotImplementedError

# --------------------------------------------------------------------

COMMAND_TO_FUNCTION: dict[str, Callable[[list[str]], str]] = {
    "/draw": draw,
    "/conjure": conjure,
    "/ping": ping,
    "/block": block,
    "/shuffle": shuffle,
    "/randint": randint,
    "$deck": test_deck
}

while True:
    command: str = input("\n>>> ")
    command_parts: list[str] = command.split(" ")
    try:
        if command == "/start":
            start()
        elif command == "/end":
            print("\nGoodbye.")
            break
        elif command_parts[0] in COMMAND_TO_FUNCTION:
            result: str = COMMAND_TO_FUNCTION[command_parts[0]](command_parts[1:])
            print(f"\n{result}")
        else:
            print("\nInvalid command.")
    except Exception:
        print("\nAn error has occurred.")