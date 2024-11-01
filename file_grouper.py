for i in range(26, 50 + 1):
    with open("minna_no_nihongo2_deck.txt", "a", encoding="utf-8") as f1:
        with open(f"folder/Minna_no_nihongo_2.{i}.txt", 'r', encoding="utf-8") as f2:
            lines = f2.read().strip().split("\n")
        for word in lines:
            if '#' not in word:
                f1.write(word + '\n')
