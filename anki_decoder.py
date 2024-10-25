from googletrans import Translator


def formater(word: str):
    word = word.replace('[', '').replace(']', '')
    word = word.replace('/', '').replace(' ', '', 1)
    return word


with open('chapter30mnn4.txt', encoding='utf8') as f:
    text = f.read().strip().split('\n')

translator = Translator()
deck = []
output_file = "new_deck.txt"

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

        deck.append([front_side, back_side_hiragana, back_side_english, back_side_russian])

for card in deck:
    print(card)
