"""Simple Substitution Cipher"""

## MODUELS ##
import re
import copy
import random
from utils.file_loader import load_dictionary

## CONSTANTS ##
WORDS = load_dictionary()
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
non_letters_or_space_pattern = re.compile(r'[^A-Z\s]', re.IGNORECASE)

## FUNCTIONS ##
def simple_get_random_key():
    """Returns a random key"""
    key = list(LETTERS)
    random.shuffle(key)
    return "".join(key)

def key_is_valid(key):
    """Checks if key is valid"""
    return sorted(key.upper()) == sorted(LETTERS)

def get_word_pattern(word):
    """Returns the word pattern"""
    word = word.upper()
    next_num = 0
    letter_nums = {}
    word_pattern = []
    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])
    return ".".join(word_pattern)

def get_all_word_patterns():
    """Returns all the word patterns from dictionary.txt"""
    all_patterns = {}
    for word in WORDS:
        pattern = get_word_pattern(word)
        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)
    return all_patterns

all_patterns = get_all_word_patterns()

def get_blank_cipher_letter_mapping():
    """Returns a dictionary value that is a blank cipherletter mapping"""
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
        'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
        'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
        'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

def add_letters_to_mapping(letter_mapping, cipherword, candidate):
    """Adds letter to mapping"""
    for i in range(len(cipherword)):
        if candidate[i] not in letter_mapping[cipherword[i]]:
            letter_mapping[cipherword[i]].append(candidate[i])

def intersect_mappings(map_a, map_b):
    """Returns the intersected map"""
    intersected_mapping = get_blank_cipher_letter_mapping()
    for letter in LETTERS:
        if map_a[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_b[letter])
        elif map_b[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(map_a[letter])
        else:
            for mapped_letter in map_a[letter]:
                if mapped_letter in map_b[letter]:
                    intersected_mapping[letter].append(mapped_letter)
    return intersected_mapping

def remove_solved_letters_from_mappings(letter_mapping):
    """Removes any solved letters from mappings"""
    loop_again = True
    while loop_again:
        loop_again = False
        solved_letters = []
        for cipherletter in LETTERS:
            if len(letter_mapping[cipherletter]) == 1:
                solved_letters.append(letter_mapping[cipherletter][0])
        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipherletter]) != 1 and s in letter_mapping[cipherletter]:
                    letter_mapping[cipherletter].remove(s)
                    if len(letter_mapping[cipherletter]) == 1:
                        loop_again = True
    return letter_mapping

def simple_substitution(message, key, mode):
    """Returns the encrypted/decrypted text"""
    translated = ''
    chars_a = LETTERS
    chars_b = key
    if mode == 'decrypt':
        chars_a, chars_b = chars_b, chars_a
    for symbol in message:
        if symbol.upper() in chars_a:
            sym_index = chars_a.find(symbol.upper())
            if symbol.isupper():
                translated += chars_b[sym_index].upper()
            else:
                translated += chars_b[sym_index].lower()
        else:
            translated += symbol
    return translated

def decrypt_with_cipherletter_mapping(ciphertext, letter_mapping):
    """Decrypts with the cipherletter mapping"""
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letter_mapping[cipherletter]) == 1:
            plain_letter = letter_mapping[cipherletter][0].upper()
            if plain_letter in LETTERS:
                key_index = LETTERS.index(plain_letter)
                key[key_index] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), "_")
            ciphertext = ciphertext.replace(cipherletter.upper(), "_")
    key = "".join(key)
    return simple_substitution(ciphertext, key, 'decrypt')

def hack_simple(message):
    """Hacks the simple sub"""
    intersected_map = get_blank_cipher_letter_mapping()
    cipherword_list = non_letters_or_space_pattern.sub("", message.upper()).split()
    for cipherword in cipherword_list:
        candidate_map = get_blank_cipher_letter_mapping()
        word_pattern = get_word_pattern(cipherword)
        if word_pattern not in all_patterns:
            continue
        for candidate in all_patterns[word_pattern]:
            add_letters_to_mapping(candidate_map, cipherword, candidate)
        intersected_map = intersect_mappings(intersected_map, candidate_map)
    return remove_solved_letters_from_mappings(intersected_map)
