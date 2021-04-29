from random import choice


def hangman():
    random_word = choice(['python', 'java', 'kotlin', 'javascript'])
    word_so_far = list('-' * len(random_word))
    tries = 8
    guessed_letters = set()

    print('H A N G M A N\n')
    while True:
        print(''.join(word_so_far))


        letter = input('Input a letter: ')

        if not len(letter) == 1:
            print('You should input a single letter')
        elif not letter.islower():
            print('Please enter a lowercase English letter')
        elif letter in guessed_letters:
            print("You've already guessed this letter")
        elif letter not in random_word:
            print("That letter doesn't appear in the word")
            tries -= 1

        if '-' not in word_so_far:
            print('You guessed the word!')
            print('You survived!')
            break
        elif tries == 0:
            print('You lost!')
            break

        guessed_letters.add(letter)

        print()

        i = 0
        while True:
            index = random_word.find(letter, i)
            if index == -1:
                break
            word_so_far[index] = letter
            i = index + 1

while True:
    action = input('Type "play" to play the game, "exit" to quit: ')
    if action == 'play':
        hangman()
    elif action == 'exit':
        break
