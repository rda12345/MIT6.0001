# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Define a list L which will contain the permutations
    L = [] 
    # Define a base case, a sequence of one letter is the same letter
    #print(sequence)
    if len(sequence)==1:
        L.append(sequence)
        return L
    # Otherwise define the recursive function, getting a sequence dividing the sequence
    # to the first letter and the rest of the sequence.
    else:
        L_sub = get_permutations(sequence[1:len(sequence)])  # a list with all the permutation of sequence(1:len(sequence))
        letter = sequence[0]
        # run over all the sequences in L_sub
        for temp_seq in L_sub:
            # for each sequence insert the first letter in sequence in all the places
            for index in range(len(temp_seq)+1):
                L.append (temp_seq[:index] + letter + temp_seq[index:])  
        # return the list
        return L
    
    
   

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    sequence = 'abcd'
    L = get_permutations(sequence)
    print(L)

