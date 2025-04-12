"""Vigenere Cipher"""

## MODULES ##
import itertools
import re
from random import choice, shuffle
from utils.file_loader import load_dictionary
from utils import frequency_analysis
from utils import detect_english


## CONSTANTS ##
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 16
NONLETTERS_PATTERN = re.compile("[^A-Z]")
ENGLISH_WORDS = load_dictionary()

def vigenere_get_random_key():
    """Returns a random key"""
    key = list(choice(list(ENGLISH_WORDS))) # Grabs a random word from the dictionary to use as the key
    shuffle(key) # Shuffles the random word from the dictionary
    key = ''.join(key)
    return key

def vigenere_encrypt(message, key):
    """Function to encrypt vigenere cipher"""
    return translate_message(message, key, "encrypt")

def vigenere_decrypt(message, key):
    """Function to decrypt vigenere cipher"""
    return translate_message(message, key, "decrypt")

def translate_message(message, key, mode):
    """Function to translate message"""
    translated = []
    key_index = 0
    key = key.upper()
    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == "encrypt":
                num += LETTERS.find(key[key_index])
            elif mode == "decrypt":
                num -= LETTERS.find(key[key_index])
            num %= len(LETTERS)
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            key_index += 1
            if key_index == len(key):
                key_index = 0
        else:
            translated.append(symbol)
    return "".join(translated)

def find_repeat_sequence_spacing(message):
    """
    Function to go through the message and find any three to five letter sequences
    that are repeated. Returns the dictionary set with the keys of the sequence and values
    of a list of spacings.
    """
    message = NONLETTERS_PATTERN.sub('', message.upper())
    seq_spacings = {}
    for seq_len in range(3, 6):
        for seq_start in range(len(message) - seq_len):
            seq = message[seq_start:seq_start + seq_len]
            for i in range(seq_start + seq_len, len(message) - seq_len):
                if message[i:i + seq_len] == seq:
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []
                    seq_spacings[seq].append(i - seq_start)
    return seq_spacings

def get_useful_factors(num):
    """
    Helper function that returns a list of useful factors of num.
    Returns a list of factors. Sets the factors as a set first to remove duplicates.
    """
    if num < 2:
        return []
    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            other_factor = int(num / i)
            if other_factor < MAX_KEY_LENGTH + 1 and other_factor != 1:
                factors.append(other_factor)
    return list(set(factors))

def get_item_at_index_one(items):
    """Helper function to get index one."""
    return items[1]

def get_most_common_factors(seq_factors):
    """
    Function to get how many times a factor occurs in seq_factors.
    Returns the factors_by_count.
    """
    factor_counts = {}
    for seq in seq_factors:
        factor_list = seq_factors[seq]
        for factor in factor_list:
            if factor not in factor_counts:
                factor_counts[factor] = 0
            factor_counts[factor] += 1
    factors_by_count = []
    for factor, count in factor_counts.items():
        if factor <= MAX_KEY_LENGTH:
            factors_by_count.append((factor, count))
    factors_by_count.sort(key=get_item_at_index_one, reverse=True)
    return factors_by_count

def kasiski_examination(ciphertext):
    """
    Function to find out the sequences of three 
    to five letters that occur multiple times in ciphertext.
    """
    repeated_seq_spacings = find_repeat_sequence_spacing(ciphertext)
    seq_factors = {}
    for seq, spacings in repeated_seq_spacings.items():
        seq_factors[seq] = []
        for spacing in spacings:
            seq_factors[seq].extend(get_useful_factors(spacing))
    factors_by_count = get_most_common_factors(seq_factors)
    all_likely_key_lengths = []
    for two_int_tuple in factors_by_count:
        all_likely_key_lengths.append(two_int_tuple[0])
    return all_likely_key_lengths

def get_nth_subkeys_letters(nth, key_length, message):
    """Returns every nth letter for each key_length set of letters in text."""
    message = NONLETTERS_PATTERN.sub('', message)
    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += key_length
    return ''.join(letters)

def attempt_hack_with_key_length(ciphertext, most_likely_key_length):
    """Function to determine the most likely letters for each letter in the key."""
    ciphertext_up = ciphertext.upper()
    all_freq_scores = []
    for nth in range(1, most_likely_key_length + 1):
        nth_letters = get_nth_subkeys_letters(nth, most_likely_key_length, ciphertext_up)
        freq_scores = []
        for possible_key in LETTERS:
            decrypted_text = vigenere_decrypt(nth_letters, possible_key)
            key_and_freq_match_tuple = (possible_key, frequency_analysis.english_freq_match_score(decrypted_text))
            freq_scores.append(key_and_freq_match_tuple)
        freq_scores.sort(key=get_item_at_index_one, reverse=True)
        all_freq_scores.append(freq_scores[:NUM_MOST_FREQ_LETTERS])
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=most_likely_key_length):
        possible_key = ''
        for i in range(most_likely_key_length):
            possible_key += all_freq_scores[i][indexes[i]][0]
        decrypted_text = vigenere_decrypt(ciphertext, possible_key)
        if detect_english.is_english(decrypted_text):
            orig_case = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    orig_case.append(decrypted_text[i].upper())
                else:
                    orig_case.append(decrypted_text[i].lower())
            decrypted_text = ''.join(orig_case)
        return decrypted_text, possible_key
    return None

def hack_vigenere(ciphertext):
    """
    Function to hack the ciphertext.
    Returns the hacked message.
    """
    all_likely_key_lengths = kasiski_examination(ciphertext)
    key_length_str = ''
    for key_length in all_likely_key_lengths:
        key_length_str += f'{key_length} '
    hacked_message = None
    for key_length in all_likely_key_lengths:
        hacked_message = attempt_hack_with_key_length(ciphertext, key_length)
        if hacked_message is not None:
            break
    if hacked_message is None:
        for key_length in range(1, MAX_KEY_LENGTH + 1):
            if key_length not in all_likely_key_lengths:
                hacked_message = attempt_hack_with_key_length(ciphertext, key_length)
                if hacked_message is not None:
                    break
    return hacked_message