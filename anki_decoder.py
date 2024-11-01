import argparse
import os

import magic
from googletrans import Translator


def check_file_extension(file_name: str) -> str:
    """
    Checks if the file is a text file based on extension or MIME type.

    Args:
        file_name (str): The name of the file to check.

    Returns:
        str: Validated filename with .txt extension if applicable, else None.
    """
    if file_name.endswith(".txt"):
        return file_name
    elif os.path.exists(file_name) and magic.from_file(file_name, mime=True) == "text/plain":
        return f"{file_name}.txt"
    return None


def format_word(word: str) -> str:
    """
    Formats a word by removing unwanted characters for consistency.

    Args:
        word (str): The word to format.

    Returns:
        str: Formatted word.
    """
    return word.replace('[', '').replace(']', '').replace('/', '').lstrip()


def create_deck(input_file_name: str):
    """
    Reads an input file and creates a deck of words with translations.

    Args:
        input_file_name (str): The name of the input file containing words.

    Returns:
        list: A deck list of formatted word entries, or None if file not found.
    """
    try:
        with open(input_file_name, encoding='utf8') as file:
            lines = file.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_name}' not found.")
        return None

    translator = Translator()
    deck = []

    for line in lines:
        if "#" in line:  # Ignore comments
            continue

        card_parts = line.split()
        if len(card_parts) < 2:
            print(f"Warning: Skipping malformed line: '{line}'")
            continue

        front = card_parts[0]
        back_hiragana = format_word(card_parts[1])
        back_english = format_word(" ".join(card_parts[2:])) if len(card_parts) > 2 else ''

        try:
            back_russian = ""
            for w in back_english.split():
                back_russian += translator.translate(w, src='en', dest='ru').text.lower() + ' '
            back_russian = back_russian[:-1]
            back_russian += ', ' + translator.translate(front, src='ja', dest='ru').text.lower()
        except Exception as e:
            print(f"Translation error for '{front}': {e}")
            back_russian = "Translation failed"

        deck.append([front, back_hiragana, back_english, back_russian])

    return deck


def save_deck(deck: list, output_file_name: str):
    """
    Saves the deck list to the specified output file in CSV-like format.

    Args:
        deck (list): The deck to save.
        output_file_name (str): Name of the output file.
    """
    if not deck:
        print("No deck data to save.")
        return

    with open(output_file_name, "w", encoding="utf-8") as file:
        for front, hiragana, english, russian in deck:
            file.write(f"{front};{hiragana};{english};{russian}\n")
    print(f"Deck saved successfully in '{output_file_name}' for Anki import.")


def main():
    """
    Main function to parse command-line arguments, create and save the deck.
    """
    parser = argparse.ArgumentParser(description="Tool to create language learning decks")
    parser.add_argument("input_file", type=str, help="Name of the input file with word entries.")
    parser.add_argument("output_file", type=str, help="Name of the output file to save the deck.")

    args = parser.parse_args()

    input_file = check_file_extension(args.input_file)
    if not input_file:
        print(f"Error: '{args.input_file}' is not a valid text file.")
        return

    output_file = check_file_extension(args.output_file)
    if not output_file:
        print(f"Error: '{args.output_file}' is not a valid text file.")
        return

    deck = create_deck(input_file)
    save_deck(deck, output_file)


if __name__ == '__main__':
    main()
