# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list



### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text
        
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # Introducing a dictionary which will be defined by the permutation vowels_permuation
        transpose_dict = {}
        # Running over all the vowels and defining associated dictionary values according to vowels_permutation
        for case in (VOWELS_LOWER,VOWELS_UPPER):
            if case == VOWELS_UPPER:
                permutation_case = vowels_permutation.upper()
            else:
                permutation_case = vowels_permutation
            # initializing the index running over the leters in vowels permutattion
            ind = 0
            for vowel in case:
                transpose_dict[vowel] = permutation_case[ind]
                ind += 1
        # Running over all the consonants and defining associated dictionary value
        for case in (CONSONANTS_LOWER,CONSONANTS_UPPER):        
            for consonant in case:
                transpose_dict[consonant] = consonant        
        return transpose_dict
        

            
        
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        transpose_text = ""        
        # for all the letters in message for the ones in the alphabet shift them using the transposed dictionary
        for char in  self.message_text:
            if char in transpose_dict:
                transpose_text += transpose_dict[char]  
            else:
                transpose_text += char
        return transpose_text

        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)
        
        
    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # Imports the permutation using get_permutations
        permutation_list= get_permutations(VOWELS_LOWER)
        perm_score_dict = {}
        val_words = self.get_valid_words()
        
        # Runs over all permutations and checks for the number of valid words in English
        for permutation in permutation_list:
            # transpose the vowels using apply_shift class method
            transposed_dict = self.build_transpose_dict(permutation)
            deciphered_message = self.apply_transpose(transposed_dict)      
            # split the message into words and create a list containing the words
            deciphired_list = deciphered_message.split()            
            num_real_words = 0
            # check if the word is a valid word in english, if so raise the counter by one
            
            for word in deciphired_list:
                if is_word(val_words, word):
                    num_real_words += 1
            # add the total number of words to the shift score dictionary
            perm_score_dict[permutation] = num_real_words
            # retrive the best permutation giving the maximum words in english.
        best_perm = max(perm_score_dict,key = perm_score_dict.get) # best_perm is different from perm, it is essentially its 
                                                                    # reverse permutation with respect to the vowels in message_text
        max_score = perm_score_dict[best_perm]
        #print('message is: ', self.get_message_text)
        best_deciphered_message = self.apply_transpose(self.build_transpose_dict(best_perm))
        #print('in line print: ',best_deciphered_message)
        #print(self.build_transpose_dict(best_perm))
        if max_score >0:
            return best_deciphered_message
        # If no good permutations are found returns the original string
        else:
            return self.message_text
        
if __name__ == '__main__':

    
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print('--------------------------- \n')
    
    #TODO: WRITE YOUR TEST CASES HERE
    text = 'king is red together university'
    
    print('Test case for incrypting:')
    message = SubMessage(text)
    permutation = "eauio"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Kung us rad tigathar onuvarsuty")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    print('--------------------------- \n')
       
    
    print('Test case for decrypting:')
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print("Expected decryption: king is red university")
    print('--------------------------- \n')
   
    message = SubMessage(text)
    permutation = "uaieo"
    enc_dict = message.build_transpose_dict(permutation)
    
    print('Test case for decrypting:')
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print("Expected decryption: king is red university")
    print('--------------------------- \n')
   
