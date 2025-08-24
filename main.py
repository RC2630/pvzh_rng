from __future__ import annotations
from io import TextIOWrapper as File
from json import load as json_to_dict
from typing import Any, Callable
from random import randint as lib_randint

# --------------------------------------------------------------------

class Card:

    def __init__(self: Card, info: dict[str, Any]) -> None:
        self.name: str = info["name"]
        self.side: str = info["side"]
        self.tribe_list: list[str] = info["tribes"]
        self.set: str = info["set"]
        self.type: str = info["type"]
        self.cost: int = info["cost"]
        self.rarity: str = info["rarity"]
        self.is_superpower: bool = "superpower" in info["tags"]
        self.is_amphibious: bool = "amphibious" in info["traits"]
        self.is_gravestone: bool = "gravestone" in info["traits"]
        self.is_conjurable: bool = not "unconjurable" in info["tags"]

    def is_available(self: Card) -> bool:
        return self.cost != -1 and self.is_conjurable
    
    def has_one_of_tribes(self: Card, acceptable_tribes: list[str]) -> bool:
        for tribe in acceptable_tribes:
            if tribe in self.tribe_list:
                return True
        return False
    
    def __str__(self: Card) -> str:
        attribute_exclusion_list: list[str] = ["name", "is_available", "has_one_of_tribes"]
        result: str = f"name = {self.name}\n"
        for attribute in dir(self):
            if not attribute.startswith("__") and attribute not in attribute_exclusion_list:
                result += f"{attribute} = {eval(f'self.{attribute}')}\n"
        result += f"is_available = {self.is_available()}"
        return result

    def __repr__(self: Card) -> str:
        return self.__str__()

# --------------------------------------------------------------------

cards_file: File = open("reference/cards.json", "r")
ALL_CARDS: list[Card] = [Card(card) for card in json_to_dict(cards_file)["cards"]]
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

def is_number(x: Any) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False

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

def test_cards(args: list[str]) -> str:
    result: str = ""
    for i in range(int(args[0])):
        ri: int = random_index(ALL_CARDS)
        result += f"{ALL_CARDS[ri]}\n\n"
    return result[:-2]

# --------------------------------------------------------------------

def start() -> None:
    
    global DECK, SUPERPOWERS

    def reroll_msg(i: int) -> str:
        return "" if slots[i]["rerolled"] else " (available for reroll)"

    def get_reroll_input() -> str:
        response: str = input("\nEnter the slot number for the card that you want to reroll, "
                              "or \"pass\" to start the match: ")
        acceptable_responses: list[str] = [str(slot) for slot in rerollable_slots] + ["pass"]
        while response not in acceptable_responses:
            response = input("That is not valid. Try again: ")
        return response

    slots: dict[int, dict[str, Any]] = {
        i: {"card": "", "rerolled": False} for i in range(1, 5)
    }

    for i in range(1, 5):
        ri: int = random_index(DECK)
        card: str = DECK[ri]
        del DECK[ri]
        slots[i]["card"] = card

    print(f"\nYour starting four cards are:\n")
    for i in range(1, 5):
        print(f"{i}: {slots[i]["card"]}{reroll_msg(i)}")

    rerollable_slots: list[int] = list(range(1, 5))
    reroll_input: str = get_reroll_input()
    
    while reroll_input != "pass":

        reroll_slot: int = int(reroll_input)
        ri_reroll: int = random_index(DECK)
        card_reroll: str = DECK[ri_reroll]
        del DECK[ri_reroll]
        DECK.append(slots[reroll_slot]["card"])
        slots[reroll_slot]["card"] = card_reroll
        slots[reroll_slot]["rerolled"] = True
        del rerollable_slots[rerollable_slots.index(reroll_slot)]

        print(f"\nYour new starting four cards are:\n")
        for i in range(1, 5):
            print(f"{i}: {slots[i]["card"]}{reroll_msg(i)}")

        if not all([slots[i]["rerolled"] for i in range(1, 5)]):
            reroll_input = get_reroll_input()
        else:
            reroll_input = "pass"

    super_ri = random_index(SUPERPOWERS)
    starting_superpower: str = SUPERPOWERS[super_ri]
    del SUPERPOWERS[super_ri]
    print(f"\nYour starting superpower is {starting_superpower}.")

# --------------------------------------------------------------------

def conjure(args: list[str]) -> str:
    
    conjure_set: list[Card] = [card for card in ALL_CARDS if card.is_available()]

    if "amphibious" in args:
        conjure_set = [card for card in conjure_set if card.is_amphibious]

    if "gravestone" in args:
        conjure_set = [card for card in conjure_set if card.is_gravestone]

    if "superpower" in args:
        conjure_set = [card for card in conjure_set if card.is_superpower]
    else:
        conjure_set = [card for card in conjure_set if not card.is_superpower]

    key_value_pairs: dict[str, str] = {}
    for arg in args:
        if ":" in arg:
            key_value_split: list[str] = arg.split(":")
            key_value_pairs[key_value_split[0]] = key_value_split[1]

    for key, value in key_value_pairs.items():

        if key == "side":
            conjure_set = [card for card in conjure_set if card.side == value]
        elif key == "set":
            conjure_set = [card for card in conjure_set if card.set == value]
        elif key == "type":
            conjure_set = [card for card in conjure_set if card.type == value]
        elif key == "rarity":
            conjure_set = [card for card in conjure_set if card.rarity == value]

        elif key == "tribe":
            acceptable_tribes: list[str] = value.split("|")
            conjure_set = [
                card for card in conjure_set if card.has_one_of_tribes(acceptable_tribes)
            ]

        elif key == "cost":
            if value.startswith("<="):
                maximum: int = int(value[2:])
                conjure_set = [card for card in conjure_set if card.cost <= maximum]
            elif value.startswith(">="):
                minimum: int = int(value[2:])
                conjure_set = [card for card in conjure_set if card.cost >= minimum]
            else:
                exact_cost: int = int(value)
                conjure_set = [card for card in conjure_set if card.cost == exact_cost]

    if len(conjure_set) == 0:
        return "No cards can be conjured based on these criteria."
    
    count: int = int(args[-1]) if is_number(args[-1]) else 1
    result: list[str] = []
    for i in range(count):
        ri: int = random_index(conjure_set)
        result.append(conjure_set[ri].name)
    
    return ", ".join(result)

# --------------------------------------------------------------------

COMMAND_TO_FUNCTION: dict[str, Callable[[list[str]], str]] = {
    "/draw": draw,
    "/conjure": conjure,
    "/ping": ping,
    "/block": block,
    "/shuffle": shuffle,
    "/randint": randint,
    "$deck": test_deck,
    "$cards": test_cards
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