"""Detect English Module"""

## MODULES ##
from utils.file_loader import load_dictionary

## CONSTANTS ##
UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'
ENGLISH_WORDS = load_dictionary()

## FUNCTIONS ##
def get_english_count(message):
    """Returns english count"""
    message = message.upper()
    message = remove_non_letters(message)
    possible_words = message.split()
    if possible_words == []:
        return 0.0
    matches = 0
    for word in possible_words:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possible_words)

def remove_non_letters(message):
    """Function to remove non letters"""
    letters_only = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            letters_only.append(symbol)
    return ''.join(letters_only)

def is_english(message, word_percentage=20, letter_percentage=85):
    """Function to detect english"""
    words_match = get_english_count(message) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message))
    message_letters_percentage = float(num_letters) / len(message) * 100
    letters_match = message_letters_percentage >= letter_percentage
    return words_match and letters_match
