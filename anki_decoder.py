from googletrans import Translator


def formater(word: str):
    word = word.replace('[', '').replace(']', '')
    word = word.replace('/', '').replace(' ', '', 1)
    return word


def deck_creation(input_file_name: str):
    try:
        with open(input_file_name, encoding='utf8') as f:
            text = f.read().strip().split('\n')
    except FileNotFoundError:
        return None

    translator = Translator()
    deck = []

    for card in text:
        if card[0] != '#':

            card = card.split()

            front_side = card[0]
            back_side_hiragana = formater(card[1])
            back_side_english = ''
            back_side_russian = ''
            for i in range(2, len(card)):
                back_side_english = back_side_english + ' ' + card[i]
            back_side_english = formater(back_side_english)
            for word in back_side_english.split(', '):
                back_side_russian += ' ' + translator.translate(word, src='en', dest='ru').text
            back_side_russian = formater(back_side_russian)

            deck.append([front_side, back_side_hiragana, back_side_english, back_side_russian])

    return deck


def file_saving(deck: list, output_file_name: str):
    if deck is None:
        print("Input file not found!")
        return

    for card in deck:
        print(card)

    n = input("Save this deck? y/n \n")

    if n.strip().lower() == "y":
        with open(output_file_name, "w", encoding="utf-8") as file:
            for side1, side2_hi, side2_en, side2_ru in deck:
                file.write(f"{side1};{side2_hi};{side2_en};{side2_ru}\n")
        print('Success. Now you can import this deck to Anki.')
    elif n.strip().lower() == "n":
        print("Saving cancelled.")


def main():
    input_file_name = input("Input file name: ")
    output_file_name = input("Output file name: ")

    deck = deck_creation(input_file_name)
    file_saving(deck, output_file_name)


if __name__ == '__main__':
    main()
