"""Affine Cipher"""

### IMPORT MODULES ###

from random import randint
from utils.file_loader import load_dictionary

### CONSTANTS ###

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWZXYabcdefghijklmnopqrstuvwxyz1234567890 '?!.,"
WORDS = load_dictionary()
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

### FUNCTIONS ###

def gcd(a,b):
    """Retruns greatest common divisor"""
    while a != 0:
        a, b = b % a, a
    return b

def find_mod_inverse(a, m):
    """Returns the modualar inverse"""
    if gcd(a, m) != 1:
        return 1
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def affine_get_random_key():
    """Generates random keys."""
    while True:
        key_a = randint(2, len(SYMBOLS))
        key_b = randint(2, len(SYMBOLS))
        if gcd(key_a, len(SYMBOLS)) == 1:
            return key_a * len(SYMBOLS) + key_b

def get_key_parts(key):
    """Returns the key parts of the key"""
    key_a = key // len(SYMBOLS)
    key_b = key % len(SYMBOLS)
    return (key_a, key_b)

def checkKeys(key_a, key_b, mode):
    if key_a == 1 and mode == "E":
        raise ValueError("Cipher is weak if key A is 1. Choose a different key.")
    if key_b == 0 and mode == "E":
        raise ValueError("Cipher is weak if key B is 0. Choose a different key.")
    if key_a < 0 or key_b < 0 or key_b > len(SYMBOLS) - 1:
        raise ValueError("Key A must be greates than 0 and key B must be between 0 and %s." % (len(SYMBOLS) - 1))
    if gcd(key_a, len(SYMBOLS)) != 1:
        raise ValueError("Key A (%s) and symbol set size (%s) are not relatively prime. Choose a different key." % (key_a, len(SYMBOLS)))

def affine_encrypt(plaintext, key):
    """Encrypts with affine cipher"""
    key_a, key_b = get_key_parts(key)
    ciphertext = ""
    for char in plaintext:
        if char in SYMBOLS:
            char_index = SYMBOLS.find(char)
            ciphertext += SYMBOLS[(char_index * key_a + key_b) % len(SYMBOLS)]
        else:
            ciphertext += char
    return ciphertext

def affine_decrypt(ciphertext, key):
    """Decrypts with affine cipher"""
    key_a, key_b = get_key_parts(key)
    plaintext = ""
    mod_inverse_of_key_a = find_mod_inverse(key_a, len(SYMBOLS))
    for char in ciphertext:
        if char in SYMBOLS:
            char_index = SYMBOLS.find(char)
            plaintext += SYMBOLS[(char_index - key_b) * mod_inverse_of_key_a % len(SYMBOLS)]
        else:
            plaintext += char
    return plaintext

def affine_hack(ciphertext):
    """Hacks the affine cipher"""
    best_key = 0
    best_translation = ""
    best_score = 0
    for key in range(len(SYMBOLS) ** 2):
        key_a = get_key_parts(key)[0]
        if gcd(key_a, len(SYMBOLS)) != 1:
            continue
        answer = affine_decrypt(ciphertext, key)
        words_found = sum(1 for word in answer.split() if word.lower() in WORDS)
        if words_found > best_score:
            best_score = words_found
            best_key = key
            best_translation = answer
    return best_translation, best_key
