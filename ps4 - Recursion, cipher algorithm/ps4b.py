# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        # define the getter methods:
        # returns an immutable string with the text
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return  self.message_text
        # returns a copy of valid_words
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        # retruns a copy of self.valid_words()            
        return self.valid_words.copy() 

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # ​ascii_lowercase/_uppercase from module string containes all the lower/upper case letters from a to z.
        alphabet_lower = string.ascii_lowercase
        alphabet_upper = string.ascii_uppercase
        # Defining the dictionary of shifted letters.
        shifted_lett_dict = {}
        
        # For all the lower and uppercase letters
        for alphabet in (alphabet_lower,alphabet_upper):
            # For each letter in the alphabet
            for letter in alphabet:
                ind = alphabet.index(letter)
                
                # If ind + shift is larger than the length of the lower/upper case alphabet
                if (ind + shift) < len(alphabet):
                    # Set the correct element in the shifted dictionary
                    shifted_lett_dict[letter] = alphabet[ind+shift] 
            
                # Otherwise appropriatly define the index of the index. 
                else:
                    new_ind = (ind+shift)%len(alphabet)
                    # Set the correct element in the shifted dictionary
                    shifted_lett_dict[letter] = alphabet[new_ind] 
        return shifted_lett_dict
      
    
                
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_text = ""
        # build the instant shifted dictionary by calling the method defined in the class
        shift_dict = self.build_shift_dict(shift)
        # for all the letters in message for the ones in the alphabet shift them using the shifted dictionary
        for char in  self.message_text:
            if char in shift_dict:
                shifted_text += shift_dict[char]  
            else:
                shifted_text += char
        return shifted_text

# def test_apply_shift(text,shift):
#     a = Message(text)    
#     print(a.apply_shift(shift))

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shifts = shift
        self.encryption_dict = self.build_shift_dict(shift) 
        self.message_text_encrypted = self.apply_shift(shift)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return  self.shift 
    
    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()
        
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted
        
    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        assert not ((0 <= shift) and (shift < 26)),"Invalid shift value entered."
        assert type(shift) != int,"Shift should be and integer."

        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(shift)
        self.message_text_encrypted = Message.apply_shift(shift)
        

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # for all the possible shifts
        shift_score_dict = {}
        for shift_value in range(0,26):
            # perform the shift on the relevant attributes using apply_shift class method 
            deciphered_message = self.apply_shift(shift_value)
            # split the message into words
            dephired_list = deciphered_message.split()
            
            num_real_words = 0
            # check if the word is a valid word in english, if so raise the counter by one
            for word in dephired_list:
                if is_word(self.valid_words, word):
                    num_real_words += 1
            # add the total number of words to the shift score dictionary
            shift_score_dict[str(shift_value)] = num_real_words
        # retrive the shift giving the maximum words in english.
        best_shift = int(max(shift_score_dict,key = shift_score_dict.get))
        decrypted_message = self.apply_shift(best_shift)    
        return (best_shift,decrypted_message)
           


       
if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
    #ciphertext = CiphertextMessage('jgnnq')
    #print('Expected Output:', (24, 'hello'))
    #print('Actual Output:', ciphertext.decrypt_message())

    # Test case for incrypting
    shift = 2
    Text_message = 'together'
    plaintext = PlaintextMessage(Text_message,shift)
    decrypted_message = plaintext.get_message_text_encrypted()
    print('Test case for incrypting:')
    print('Expected Output: vqigvjgt')
    print('Actual Output: ', decrypted_message)
    print('---------------------------')
    
    # Test case for decrypting
    print('Test case for decrypting:')
    cipher_text = CiphertextMessage(decrypted_message)
    print("Expected Output: "+"("+str(26-shift)+",'"+Text_message+"')")
    print('Actual Output: ', cipher_text.decrypt_message())
    print('---------------------------')
    
    #TODO: best shift value and unencrypted story 
    story = get_story_string()
    unecrypted_story = CiphertextMessage(story)
    
    best_shift,unencrypted_story = unecrypted_story.decrypt_message()
    print('Unencrypted story: \n', unencrypted_story)
    print('The best shift is:', best_shift)
    
    #plaintext = PlaintextMessage('hello', 2)
    #ciphertext.decrypt_message()    
    #plaintext = PlaintextMessage(story,shift)
    
    
    #pass #delete this line and replace with your code here
