import random
import sys
import json
from constants import GREEN, YELLOW, DEFAULT, CURSOR_UP, LINE_CLR

CHOSEN_WORD = None
HINT_MODE = False
hints = []


def get_random_word_details(filename):
    '''
    Gets a random word and its related information(synonyms,
    antonyms, meanings, examples) from filename

    filename has this infomation in json encoded format
    '''
    with open(filename, 'r') as f:
        word_infos = f.readlines()

    return json.loads(random.choice(word_infos).strip())


def get_hint():
    '''
    Provide a hint to help the player
    '''
    sorry_msg = "Oops. No hints available"
    if hints:
        return hints.pop()
    else:
        return sorry_msg


def cursor_up_line_clear(n=1):
    '''
    Moves the terminal cursor n lines up and
    removes any existing data on the lines
    '''
    print((CURSOR_UP + LINE_CLR)*n, end="")


def invalidate(guess):
    '''
    Checks if a guess is invalid. A guess is invalid
    if it does not have proper length or has non-alphabetic
    chars or is asking for a hint

    Return value is an appropriate string indicating the reason
    of invalidation. If the guess is valid, False if returned.
    '''
    if guess.lower() == 'hint' and HINT_MODE:
        return 'hint'
    if len(guess) != 5:
        return 'Please make a guess that is 5 characters long'
    elif not guess.isalpha():
        return 'Non Alphabetic guesses not allowed'
    else:
        return False


def take_guess():
    '''
    Prompts the user for a guess until they
    enter a valid guess (5 English alphabets)
    '''

    bad_input = False
    guess = input()

    while invalidate(guess):
        cursor_up_line_clear(2 if bad_input else 1)
        bad_input = True
        print(invalidate(guess) if invalidate(guess) != 'hint' else get_hint())
        guess = input()

    cursor_up_line_clear(2 if bad_input else 1)
    return guess


def play(word):
    '''
    Main Loop  of the game.
    '''

    print('Guess the five letter word')
    for attempt in range(6):
        guess = take_guess()
        for idx, letter in enumerate(guess):
            letter_small = letter.lower()
            if letter_small == word[idx]:
                print(GREEN + letter + DEFAULT, end="")
            elif letter_small in word:
                print(YELLOW + letter + DEFAULT, end="")
            else:
                print(letter, end="")
        print()

        if guess.lower() == word:
            print('WOW YOU WON')
            return 1
    print("SORRY YOU LOST.")


if __name__ == '__main__':
    print("Starting...")
    CHOSEN_WORD_DETAILS = get_random_word_details("dictionary.txt")

    if len(sys.argv) > 1 and sys.argv[1] == "--hint-mode":
        HINT_MODE = True

    # Note that order is important here
    word, synonyms, antonyms, definitions, examples = \
        CHOSEN_WORD_DETAILS.values()

    hints.append("Synonyms: " + ", ".join(synonyms))
    hints.append("Antonyms: " + ", ".join(antonyms))

    cursor_up_line_clear()
    play(word)

    print(f"Word: {word}", end="\n\n")
    print("Meanings: \n" + "\n".join(definitions), end="\n\n")
    print("Usage: \n" + "\n".join(examples), end="\n\n")
