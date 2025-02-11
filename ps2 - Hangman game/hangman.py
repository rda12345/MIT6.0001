# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # If the user enters multiple times the same letters the following function
    # should give a wrong result.
    return sorted(secret_word) == sorted(letters_guessed)
    


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    updated_list = list(secret_word)
    for index in range(len(secret_word)):
        char1 = secret_word[index]
        updated_list[index] = '_ '
        for char2 in letters_guessed:
            if char1==char2:
                updated_list[index] = char2 # updates letters guessed 
    updated_word = ''.join(updated_list)
    return updated_word            



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    unguessed_letters_list = list('abcdefghijklmnopqrstuvwxyz')
    if letters_guessed == []:
        return ''.join(unguessed_letters_list)
    else:
        for char in letters_guessed:
            unguessed_letters_list.remove(char)
            unguessed_letters = ''.join(unguessed_letters_list)
        return unguessed_letters    
    
    

#letter_list = "abcdefghijklmnopqrstuvwxyz"
#secret_word = choose_word(wordlist)     # This is just for the initial stage
secret_word = 'else'
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    ln_secret_word = len(secret_word)    
    letters_guessed = []
    guesses = 6
    warning = 3
    unique_letters = 0
    vowels = 'aeuou'
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word which is ", ln_secret_word ," letters long.")
    print("You have", warning ,"warnings left.")
    print("-----------")
    while guesses>0:
        print("You have ", guesses ,"guesses left.")
        print("Available letters: "+ get_available_letters(letters_guessed))
        letter_temp = input("Please guess a letter: ")
        letter = str.lower(letter_temp)
        if letter == '':    # checks if the user entered nothing, then leades to a warning
            letter = '1'    
        if (letter in letters_guessed) or (letter not in get_available_letters(letters_guessed)):   # checks if the letter has been previously
                                                                                                    # guessed or not in the alphabet
            warning -= 1
            partially_guessed_word = get_guessed_word(secret_word, letters_guessed)    
            print("Oops! You've already guessed that letter. You now have ", warning, " warnings left:", partially_guessed_word) 
        else:    
            letters_guessed.append(letter) 
            partially_guessed_word = get_guessed_word(secret_word, letters_guessed)    
            if letter in secret_word:  # the good guess case
                print("Good guess: ", partially_guessed_word)
                unique_letters += 1
                if '_ ' not in partially_guessed_word:
                    print('Congratulations, you won!')
                    total_score = guesses*unique_letters
                    print('Your total score for this game is: ', total_score)
                    break
            else: # the bad guess case
                    print("Oops! That letter is not in my word: ", partially_guessed_word) 
                    if letter in vowels:
                        guesses -= 2
                    else:
                        guesses -= 1
        if warning == 0:
            print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", partially_guessed_word)
            guesses -= 1
            warning = 3
        
        print("-----------")
    if guesses == 0:
        print("Sorry, you ran out of guesses. The word was "+secret_word+".")
        
    
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    strip_my_word = my_word.replace(" ","")
    if len(strip_my_word) != len(other_word):
        #print(len(strip_my_word))
        return False
    else:
        for i in range(len(strip_my_word)):
            char = strip_my_word[i]
            if char != other_word[i] and char !='_':
                return False
                break
        return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_words = ''
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_words = possible_words +' '+word
    return possible_words.strip()       
            



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    ln_secret_word = len(secret_word)    
    letters_guessed = []
    guesses = 6
    warning = 3
    unique_letters = 0
    vowels = 'aeuou'
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word which is ", ln_secret_word ," letters long.")
    print("You have", warning ,"warnings left.")
    print("-----------")
    while guesses>0:
        print("You have ", guesses ,"guesses left.")
        print("Available letters: "+ get_available_letters(letters_guessed))
        letter_temp = input("Please guess a letter: ")
        letter = str.lower(letter_temp)
        if letter == '*':               # provides the hint
            partially_guessed_word = get_guessed_word(secret_word, letters_guessed)    
            print("Possible word matches are: "+show_possible_matches(partially_guessed_word))
        else:
            if letter == '':    # checks if the user entered nothing, then leades to a warning
                  letter = '1'    
            if (letter in letters_guessed) or (letter not in get_available_letters(letters_guessed)):   # checks if the letter has been previously
                warning -= 1
                partially_guessed_word = get_guessed_word(secret_word, letters_guessed)    
                print("Oops! You've already guessed that letter. You now have ", warning, " warnings left:", partially_guessed_word) 
            else:    
                letters_guessed.append(letter) 
                partially_guessed_word = get_guessed_word(secret_word, letters_guessed)    
                if letter in secret_word:  # the good guess case
                    print("Good guess: ", partially_guessed_word)
                    unique_letters += 1
                    if '_ ' not in partially_guessed_word:
                        print('Congratulations, you won!')
                        total_score = guesses*unique_letters
                        print('Your total score for this game is: ', total_score)
                        break
                else: # the bad guess case
                    print("Oops! That letter is not in my word: ", partially_guessed_word) 
                    if letter in vowels:
                        guesses -= 2
                    else:
                        guesses -= 1
            if warning == 0:
                print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", partially_guessed_word)
                guesses -= 1
                warning = 3
            if guesses == 0:
                print("Sorry, you ran out of guesses. The word was "+secret_word+".")
        print("-----------")
            


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
     pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
#secret_word = choose_word(wordlist)
secret_word = 'apple'
hangman_with_hints(secret_word)
