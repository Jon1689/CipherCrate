"""Transposition Cipher"""

## MODULES ##
from utils.file_loader import load_dictionary

## CONSTANTS ##

WORDS = load_dictionary()

## FUNCTIONS ##

def transpo_encrypt(message, key):
    """Encrypts with transposition cipher."""
    ciphertext = [""] * key

    for column in range(key):
        current_index = column

        while current_index < len(message):
            ciphertext[column] += message[current_index]
            current_index += key

    answer = ''.join(ciphertext)
    return answer

def transpo_decrypt(message, key):
    """decrypts with the transposition cipher"""
    num_columns = key
    num_rows = -(-len(message) // key)
    num_shaded_boxes = (num_columns * num_rows) - len(message)

    cleartext = [''] * num_rows
    col = 0
    row = 0

    for symbol in message:
        cleartext[row] += symbol
        row += 1

        if row == num_rows or (row == num_rows - 1 and
                            col >= num_columns - num_shaded_boxes):
            row = 0
            col += 1

    answer = ''.join(cleartext)
    return answer

def transpo_hack(message):
    """Hacks the transposition cipher"""
    best_key = None
    best_translation = ""
    best_score = 0

    for key in range(1, len(message)):
        answer = transpo_decrypt(message, key)
        words = answer.split()
        matches = sum(1 for word in words if word in WORDS or word.lower() in WORDS)
        if matches > best_score:
            best_score = matches
            best_key = key
            best_translation = answer

    return (best_translation, best_key) if best_score > 0 else ("---COULDN'T HACK MESSAGE---", None)
