"""
*
*   Purpose: Generate random words and count the words per minute time.
*   Author: MiceX
*   Date: 03/09/2022
*
"""
import random
import time
from external import handler, save_stats, load_stats
import os
from datetime import datetime


class Editor:
    def __init__(self, file):
        self.words_file = file

    def removeSameLettersWord(self):
        with open(self.words_file, 'r', encoding='utf-8') as ReadFile:
            lines = ReadFile.readlines()

        for idx, line in enumerate(lines):
            line = line.rstrip('\n')
            # Removes Less than 2 characters lines
            if len(line) <= 1:
                lines[idx] = ""
                print(idx)

            # Remove lines that are 2 characters which are the same
            elif len(line) == 2:
                if line[0] == line[1]:
                    lines[idx] = ""

            # Remove same letter lines (aaaa, BBBB, qqqq)
            elif len(line) >= 3:
                prevChar = line[0]
                nextChar = line[1]
                counter = 0
                word_length = len(line)

                if prevChar == nextChar:
                    counter = 2
                    prevChar = nextChar

                    for idy, char in enumerate(line):
                        if idy >= 2:
                            if char == prevChar:
                                counter += 1
                                prevChar = char
                            else:
                                continue

                    if counter == word_length:
                        lines[idx] = ""
                    else:
                        continue

                else:
                    continue

        with open(self.words_file, 'w', encoding='utf-8') as WriteFile:
            WriteFile.writelines(lines)

    def random_words(self, words_amount):
        with open(self.words_file, 'r') as ReadFile:
            lines = ReadFile.readlines()

        if words_amount == -1:
            random_words_amount = random.randint(20, 50)
            randomWords = random.choices(lines, k=random_words_amount)
            for idx, word in enumerate(randomWords):
                randomWords[idx] = word.rstrip('\n')

            return {"WordsCount": random_words_amount, "SelectedWords": randomWords}

        elif words_amount > 0:
            randomWords = random.choices(lines, k=words_amount)
            for idx, word in enumerate(randomWords):
                randomWords[idx] = word.rstrip('\n')

            return {"WordsCount": words_amount, "SelectedWords": randomWords}

        else:
            handler(1, 31, "", "", "[-] Please choose a number bigger than 0")
            handler(1, 31, "", "reset", "")


def main(**keys):
    try:
        if not keys["file"] or not keys["option"]:
            pass
    except KeyError:
        print()
        handler(1, 31, "", "", "[-] Please add a file containing words")
        handler(1, 31, "", "reset", "")

    words_file = keys["file"]
    user_option = keys["option"]

    # Objects
    EditorObject = Editor(words_file)

    # PLAY
    if user_option == 1:
        words_amount = int(input("[!] How many words or random amount | [-1 for random] >> "))
        print('\n')
        chosen_words = EditorObject.random_words(words_amount)
        times = []
        game_stats = {"original": [], "clientChoice": []}

        for word in chosen_words['SelectedWords']:
            handler(1, 33, "", "", f"{word}")
            handler(1, 31, "", "reset", "")

            start = time.time()
            client_word = input("# ")
            end = time.time()

            times.append(end-start)
            if client_word != word:
                game_stats["original"].append(word)
                game_stats["clientChoice"].append(client_word)

        totalTime = 0
        for item in times:
            totalTime += item

        wpm = (words_amount / (totalTime/60))
        if wpm <= 0:
            wpm = 0

        print(f"\n[*] You have {int(wpm)} words/minute with {len(game_stats['original'])} mistakes.")
        print("""
[*] Your mistakes:
_____________________________________________
""")
        for num in range(len(game_stats["original"])):
            handler(1, 36, '', '', f"-Original-: {game_stats['original'][num]} | -Mistake-: {game_stats['clientChoice'][num]}")
        handler(1, 31, "", "reset", "")

        stats = {
            "date": f"{datetime.now()}",
            "wpm": int(wpm),
            "mistakesCount": len(game_stats['clientChoice']),
            "mistakes": {"original": game_stats['original'], "You Wrote": game_stats['clientChoice']},
        }
        save_stats(stats)

        # GAME FINISH
        input("\nPress any key to continue. . .")
        os.system('cls||clear')

    # Remove same letter lines
    elif user_option == 2:
        EditorObject.removeSameLettersWord()

    # Stats
    elif user_option == 3:
        print(load_stats())
        input("\nPress any key to continue. . .")
        os.system('cls||clear')

    # Exit
    elif user_option == 4:
        handler(1, 31, "", "", "[!] Program Closed . . .  ")
        exit()

    else:
        handler(1, 31, "", "", "\n[-] No such option!")
        handler(1, 31, "", "reset", "")
        time.sleep(1)
        os.system('cls||clear')


if __name__ == "__main__":
    # Menu
    os.system('cls||clear')
    handler(1, 31, "", "reset", "")

    # EXECUTE
    while True:
        handler(1, 32, "", "", f"""
[*] Typie is a typing test written in python
[*] Enjoy and train hard!

[*] OPTIONS:
    1) PLAY
    2) Remove same letter lines
    3) Stats
    4) EXIT

[*] If success has not come today, work harder to see what happens tomorrow - \n
 ----------------------------------------------------------------------------------------------
 ----------------------------------------CHOOSE AN OPTION--------------------------------------
  ----------------------------------------------------------------------------------------------""")
        handler(1, 31, "", "reset", "")
        try:
            option = int(input("\n[!] Insert your option >> "))
            main(file="./resources/englishWords.txt", option=option)
        except ValueError:
            handler(1, 31, "", "", "\n[-] No such option!")
            time.sleep(1)
            os.system('cls||clear')
            handler(1, 31, "", "reset", "")
