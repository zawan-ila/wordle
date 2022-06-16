import random
from constants import GREEN, YELLOW, DEFAULT, CURSOR_UP, LINE_CLR


def get_random_word(filename):
    '''
    Gets a random word from filename, which is a sequence of words
    separated by newlines
    '''
    with open(filename, 'r') as f:
        words = f.readlines()

    return random.choice(words).strip()


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
    chars
    '''

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
        print(invalidate(guess))
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
            return
    print("SORRY YOU LOST. The WORD was", word)


if __name__ == '__main__':
    random_word = get_random_word("words.txt")
    print(random_word)
    play(random_word)
