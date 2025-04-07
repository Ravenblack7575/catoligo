#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
This python script is for caluculation of primer and probe melting temperatures
Allowed letters in oligo sequence:

```
A	Adenine 
C	Cytosine
G	Guanine
T	Thymine
U	Uracil
R	Guanine / Adenine (purine)
Y	Cytosine / Thymine (pyrimidine)
K	Guanine / Thymine
M	Adenine / Cytosine
S	Guanine / Cytosine
W	Adenine / Thymine
B	Guanine / Thymine / Cytosine
D	Guanine / Adenine / Thymine
H	Adenine / Cytosine / Thymine
V	Guanine / Cytosine / Adenine
N	Adenine / Guanine / Cytosine / Thymine

```

**Note**: in general degenerate bases, make it very difficult to calculate Tm and downstream more difficult to optimise the assay because of the wide range of possibilities and combination of bases in the oligo sequence pool. Thus it is not advisable to use too many degenerate bases in your primer or probe sequences.

**Formula** (precise):

Tm ≈ (81.5 + (16.6 * log10([Na+])) + (0.41 * (%GC))) - (675 / (oligonucleotide length))

[NA+] salt in molar concentration


"""


import math

allowed_letters = {'A', 'T', 'C', 'G', 'U', 'R', 'Y', 'K', 'M', 'S', 'W', 'B', 'D', 'H', 'V', 'N'}
ambiguous_letters = allowed_letters - {'A', 'T', 'G', 'C'}
degenerate_bases = False
salt_conc = 0.05 #salt concentration referring to Na+ is usually used at 5mM or less

def validate_sequence(sequence):
    ''' This function is for validating that the sequence doesn't contain letters outside the allowed letters
    for nucleotide representation'''

    upper_sequence = sequence.upper()
    if not all(char in allowed_letters for char in upper_sequence):
        raise ValueError("Sequence contains invalid characters.")
    if len(upper_sequence) > 50:
        raise ValueError("Sequence exceeds the maximum length of 50 nucleotides.")
    if any(char.isdigit() for char in upper_sequence):
        raise ValueError("Sequence should not contain numbers.")

    global degenerate_bases

    ambiguous_count = sum(upper_sequence.count(char) for char in ambiguous_letters)
    if ambiguous_count > 3:
        raise ValueError(f"Sequence contains more than 3 degenerate bases. Found {ambiguous_count}.")
    elif ambiguous_count > 0:
        print(f"Sequence contains degenerate bases. Found {ambiguous_count}.")
        degenerate_bases = True
    else:
        print(f"Sequence contains no degenerate bases.")

    return upper_sequence

def get_valid_sequence():
    ''' This function serves to get the input from the user, performs the check,
    outputs the sequence if the check passes, or asks the user to enter the sequence again
    if the check fails.'''

    while True:
        oligoSequence = input("Please input a primer or probe sequence (or 'cancel'): ").strip()

        if oligoSequence.lower() == 'cancel':
            print("Operation cancelled.")
            break
        try:
            validated_sequence = validate_sequence(oligoSequence)
            print("Sequence is valid.")
            return validated_sequence
        except ValueError as e:
            print(f"Error: {e}")
            correct = input("Do you want to enter a corrected sequence? (yes/no): ").lower()
            if correct != 'yes':
                print("Operation cancelled.")
                break


def generate_tm_optimized_sequences(valid_sequence):
    """
    Generates sequences optimized for maximum and minimum possible Tm
    by substituting degenerate bases.

    Args:
        valid_sequence: The input sequence string containing standard and/or
                  degenerate bases.

    Returns:
        A tuple containing two strings: (max_tm_sequence, min_tm_sequence).
    """

    max_tm_map = {
        'R': 'G', 'Y': 'C', 'S': 'G', 'W': 'A', 'K': 'G', 'M': 'C',
        'B': 'G', 'D': 'G', 'H': 'C', 'V': 'G', 'N': 'G',
        'A': 'A', 'T': 'T', 'C': 'C', 'G': 'G', 'U': 'T'
    }

    min_tm_map = {
        'R': 'A', 'Y': 'T', 'S': 'A', 'W': 'A', 'K': 'T', 'M': 'A',
        'B': 'T', 'D': 'A', 'H': 'A', 'V': 'A', 'N': 'A',
        'A': 'A', 'T': 'T', 'C': 'C', 'G': 'G', 'U': 'T'
    }

    max_tm_sequence = "".join(max_tm_map.get(base.upper(), base.upper()) for base in valid_sequence)
    min_tm_sequence = "".join(min_tm_map.get(base.upper(), base.upper()) for base in valid_sequence)

    return max_tm_sequence, min_tm_sequence


def meltingtemp(sequence):

    '''Function that makes a count of A, C, T, G of a given sequence and then calculates the melting temperature.'''

    # count the bases

    base_counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0}

    for base in sequence:
        base_counts[base] = base_counts.get(base, 0) + 1

    # get the component bases
    
    num_a = base_counts.get('A', 0)
    num_t = base_counts.get('T', 0)
    num_g = base_counts.get('G', 0)
    num_c = base_counts.get('C', 0)
    
    # calculate GC%
    
    GC_percent = ((num_g + num_c) / (num_a + num_t + num_g + num_c))*100
    
    # calculate melting temerature (Tm)
    
    Tm = (81.5 + (16.6 * math.log10(salt_conc)) + (0.41 * GC_percent)) - (675 / len(sequence))
    
    return Tm


def get_melting_temp():

    '''Function that gets the melting temperature depending on whether the input sequence has degenerate bases.'''

    if degenerate_bases == True:
    
        max_tm_sequence, min_tm_sequence = generate_tm_optimized_sequences(valid_sequence)
    
        max_melting_temp = meltingtemp(max_tm_sequence)
        min_melting_temp = meltingtemp(min_tm_sequence)
    
        print(f"The melting temperature range is between {min_melting_temp:.2f} and {max_melting_temp:.2f} degrees Celcius.")
    
    else:
    
        seq_melting_temp = meltingtemp(valid_sequence)
    
        print(f"The melting temperature of your sequence is {seq_melting_temp:.2f} degrees Celcius.")


#Program starts here:

state = True

while state == True:

    try:

        valid_sequence = get_valid_sequence()

        if valid_sequence:
            print()
            print(f"Your sequence is: {valid_sequence}")
            
        else:
            state = False
            break

        get_melting_temp()
        print()
        print()
        print()

    except:

        break



# In[ ]:




