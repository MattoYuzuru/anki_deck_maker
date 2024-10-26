from googletrans import Translator
import magic


def check_file_extension(output_file_name: str):
    '''Function that checks validity of files'''
    if output_file_name.endswith(".txt"):
        return output_file_name
    elif magic.from_file(output_file_name, mime=True) == "text/plain":
        return output_file_name + '.txt'
    else:
        return None


def formater(word: str):
    '''Function for formatting words in cards from raw text'''

    # I am taking files from minna ni nihongo n4 from http://www.denisowski.org/Japanese/MNN_2/MNN_2.html
    word = word.replace('[', '').replace(']', '')
    word = word.replace('/', '').replace(' ', '', 1)
    return word


def deck_creation(input_file_name: str):
    '''Function that crates deck'''

    # open file, None if FileNotFoundError
    try:
        with open(input_file_name, encoding='utf8') as f:
            text = f.read().strip().split('\n')
    except FileNotFoundError:
        return None

    translator = Translator()
    deck = []

    # making deck here
    for card in text:
        if card[0] != '#':

            card = card.split()

            front_side = card[0]
            back_side_hiragana = formater(card[1])
            back_side_english = ''
            for i in range(2, len(card)):
                back_side_english = back_side_english + ' ' + card[i]
            back_side_english = formater(back_side_english)
            # translation may be not accurate
            back_side_russian = translator.translate(front_side, src='ja', dest='ru').text.lower()

            deck.append([front_side, back_side_hiragana, back_side_english, back_side_russian])

    return deck


def file_saving(deck: list, output_file_name: str):
    '''Function that saves deck in file'''
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
    input_file_name = check_file_extension(input(f"Input file name: "))
    output_file_name = check_file_extension(input(f"Output file name: "))

    deck = deck_creation(input_file_name)
    file_saving(deck, output_file_name)


if __name__ == '__main__':
    main()
