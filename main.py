"""CipherCrate Main Program"""

## MODULES ##
from random import randint
from pyperclip import copy
from ciphers.reverse_cipher import reverse_cipher
from ciphers.caesar_cipher import caesar_cipher, caesar_hacker
from ciphers.transposition_cipher import (transpo_decrypt,
                                transpo_encrypt,
                                transpo_hack)
from ciphers.affine_cipher import (affine_encrypt,
                        affine_decrypt,
                        affine_hack,
                        affine_get_random_key,
                        checkKeys,
                        get_key_parts)
from ciphers.simple_sub import (key_is_valid,
                        simple_get_random_key,
                        simple_substitution,
                        hack_simple,
                        decrypt_with_cipherletter_mapping)
from ciphers.vigenere_cipher import (vigenere_encrypt,
                            vigenere_decrypt,
                            hack_vigenere,
                            vigenere_get_random_key)
from utils.frequency_analysis import (english_freq_match_score,
                                get_letter_count,
                                get_frequency_order)

## CONSTANTS ##
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

## FUNCTIONS ##
def print_banner():
    """Prints Program Banner"""
    print(r"""
#########################################################
#  ____ _       _                ____           _       #
# / ___(_)_ __ | |__   ___ _ __ / ___|_ __ __ _| |_ ___ #
#| |   | | '_ \| '_ \ / _ \ '__| |   | '__/ _` | __/ _ \#
#| |___| | |_) | | | |  __/ |  | |___| | | (_| | ||  __/#
# \____|_| .__/|_| |_|\___|_|   \____|_|  \__,_|\__\___|#
#        |_|                                            #
#########################################################
""")

def get_cipher_name(cipher_choice):
    """Returns a string of the cipher name"""
    if cipher_choice == 2:
        return "--###--Caesar Cipher--###--"
    elif cipher_choice == 3:
        return "--###--Transposition Cipher--###--"
    elif cipher_choice == 4:
        return "--###--Affine Cipher--###--"
    elif cipher_choice == 5:
        return "--###--Simple Substitution Cipher--###--"
    elif cipher_choice == 6:
        return "--###--Vigenere Cipher--###--"
    elif cipher_choice == 7:
        return "--###--Public Key Cipher--###--"
    elif cipher_choice == 8:
        return "--###--Frequency Analyzer--###--"

def get_user_choice(prompt, options):
    """Function for validating menu input"""
    while True:
        choice = input(prompt)
        if choice.isdigit() and int(choice) in options:
            return int(choice)
        print(f"{RED}Invalid choice. Please try again.{RESET}")

def get_encryption_key(cipher_choice, message):
    """Gets Encryption Key"""
    print("Select key type:")
    print("1. Random")
    print("2. Personal")
    key_type = get_user_choice(">>> ", {1,2})
    if key_type == 1: #Random Key Generators
        if cipher_choice == 2: #Caesar Cipher Random Key
            return randint(1,26)
        elif cipher_choice == 3: #Transposition Cipher Random Key
            return randint(2, len(message) // 2)
        elif cipher_choice == 4: #Affive Cipher Random Key
            return affine_get_random_key()
        elif cipher_choice == 5: #Simple Substitution Cipher Random Key
            return simple_get_random_key()
        elif cipher_choice == 6: #Vigenere Cipher Random Key
            return vigenere_get_random_key().upper()
    else: #Personal Key Prompts
        if cipher_choice == 2: #Caesar Cipher Personal Key
            while True:
                key = input("Enter a number between 1-26:\n>>> ")
                if key.isdigit() and 1 <= int(key) <= 26:
                    return int(key)
                print(f"{RED}Invalid key. Must be a number from 1 to 26.{RESET}")
        elif cipher_choice == 3: #Transposition Cipher Personal KEy
            while True:
                key = input(f"Enter a number between 2 and {(len(message) // 2)}:\n>>> ")
                if key.isdigit() and 1 < int(key) <= (len(message) // 2):
                    return int(key)
                print(f"{RED}Invalid key. Must be a number from 2 to {len(message) // 2}.{RESET}")
        elif cipher_choice == 4: #Affine Cipher Personal Key
            while True:
                key_input = input("Enter a numeric key (will be split into A and B):\n>>> ")
                if key_input.isdigit():
                    key = int(key_input)
                    key_a, key_b = get_key_parts(key)
                    try:
                        checkKeys(key_a, key_b, "E")
                        return key
                    except ValueError as e:
                        print(f"{RED}{e}{RESET}")
                else:
                    print(f"{RED}Invalid key. Must be a numeric value.{RESET}")
        elif cipher_choice == 5: #Simple Substitution Cipher Personal Key
            while True:
                key_input = input("Enter a alphabetic key:\n>>> ")
                if key_is_valid(key_input):
                    return key_input.upper()
                else:
                    print(f"{RED}Please enter a proper key. Must include all 26 letters of the alphabet.{RESET}")
        elif cipher_choice == 6: #Vigenere Cipher Personal Key
            while True:
                key = input("Enter the key you would like to use here: ")
                if key.isalpha() and len(key) < len(message):
                    break
                else:
                    print(f"{RED}Please only choose a word with no numbers and shorter than the message.{RESET}")
            return key.upper()

def handle_caesar(mode):
    """Runs Caesar Cipher"""
    message = input("Enter your message:\n>>> ")
    key = get_encryption_key(2, message) if mode in (1,2) else None
    if mode == 3:
        output, key = caesar_hacker(message)
    else:
        cipher_mode = "E" if mode == 1 else "D"
        output = caesar_cipher(message, key, cipher_mode)
    print(f"{GREEN}{output}{RESET}\n-###-COPIED TO CLIPBOARD-###-")
    copy(output)
    print(f"KEY USED: {GREEN}{key}{RESET}")

def handle_reverse():
    """Runs Reverse Cipher"""
    message = input("Enter your message:\n>>> ")
    output = reverse_cipher(message)
    copy(output)
    print(f"{GREEN}{output}{RESET}\n-###-COPIED TO CLIPBOARD-###-")

def handle_transposition(mode):  #TODO: Fix case sensitivity
    """Runs Transposition Cipher"""
    message = input("Enter your message here:\n>>> ")
    key = get_encryption_key(3, message) if mode in range(1,3) else None
    output = ""
    if mode == 3:
        output, key = transpo_hack(message)
    elif mode == 1:
        output = transpo_encrypt(message, key)
    elif mode == 2:
        output = transpo_decrypt(message, key)
    print(f"{GREEN}{output}{RESET}\n-###-COPIED TO CLIPBOARD-###-")
    copy(output)
    print(f"KEY USED: {GREEN}{key}{RESET}")

def handle_affine(mode):
    """Runs Affine Cipher"""
    message = input("Enter your message here:\n>>> ")
    key = get_encryption_key(4, message) if mode in range(1,3) else None
    if mode == 3:
        output, key = affine_hack(message)
    elif mode == 1:
        output = affine_encrypt(message, key)
    elif mode == 2:
        output = affine_decrypt(message, key)
    else:
        print(f"{RED}Invalid mode selected{RESET}")
        return
    print(f"{GREEN}{output}{RESET}\n-###-COPIED TO CLIPBOARD-###-")
    copy(output)
    print(f"KEY USED: {GREEN}{key}{RESET}")

def handle_simple(mode):
    """Runs Simple Substitution Cipher"""
    if mode == 3:
        message = input("Enter your encrypted message to hack:\n>>> ")
        mapping = hack_simple(message)
        decrypted = decrypt_with_cipherletter_mapping(message, mapping)
        print(f"{GREEN}{decrypted}{RESET}\n--###--COPIED TO CLIPBOARD--###--")
        copy(decrypted)
        return
    message = input("Enter your message here:\n>>> ")
    key = get_encryption_key(5, message)
    mode_str = "encrypt" if mode == 1 else "decrypt"
    output = simple_substitution(message, key, mode_str)
    print(f"{GREEN}{output}{RESET}\n--###--COPIED TO CLIPBOARD--###--")
    copy(output)
    if mode in (1,2):
        print(f"KEY USED: {GREEN}{key}{RESET}")

def handle_vigenere(mode):
    """Runs Vigenere Cipher"""
    if mode == 3:
        message = input("Enter your encrypted message to hack:\n>>> ")
        decrypted, key = hack_vigenere(message)
        print(f"{GREEN}{decrypted}{RESET}\n--###--COPIED TO CLIPBOARD--###--")
        copy(decrypted)
        return
    message = input("Enter your message here:\n>>> ")
    key = get_encryption_key(6, message)
    output = ""
    if mode == 1:
        output = vigenere_encrypt(message, key)
    elif mode == 2:
        output = vigenere_decrypt(message, key)
    print(f"{GREEN}{output}{RESET}\n--###--COPIED TO CLIPBOARD--###--")
    copy(output)
    print(f"KEY USED: {GREEN}{key}{RESET}")

def handle_freq_analysis():
    """Runs Frequency Analysis"""
    message = input("Please input english sentence to analyze here:\n>>> ")
    match_score = english_freq_match_score(message)
    letter_count = get_letter_count(message)
    freq_order = get_frequency_order(message)
    print(f"The frequency order of your sentense is: {GREEN}{freq_order}{RESET}")
    for key, value in letter_count.items():
        if value == 0:
            continue
        print(f"Letter: {GREEN}{key}{RESET} | Frequency: {GREEN}{value}{RESET}")
    print(f"Your match score is {GREEN}{match_score}{RESET}.")

def main():
    """MAIN FUNCTION"""
    print("Choose a cipher:")
    print("""
        1. Reverse Cipher
        2. Caesar Cipher
        3. Transpositional Cipher
        4. Affine Cipher
        5. Simple Substitution Cipher
        6. Vigenere Cipher
        7. Public Key Cipher
        8. Frequency Analysis
        """)
    cipher_choice = get_user_choice(">>> ", range(1,9))
    mode = None
    if cipher_choice == 1:
        handle_reverse()
    elif cipher_choice in range(2,7):
        print(get_cipher_name(cipher_choice))
        print("Select a mode:\n1. Encrypt\n2. Decrypt\n3. Hack")
        mode = get_user_choice(">>> ", {1,2,3})
        if cipher_choice == 2:
            handle_caesar(mode)
        elif cipher_choice == 3:
            handle_transposition(mode)
        elif cipher_choice == 4:
            handle_affine(mode)
        elif cipher_choice == 5:
            handle_simple(mode)
        elif cipher_choice == 6:
            handle_vigenere(mode)
    elif cipher_choice == 7:
        print("\nSelect a mode:\n1. Encrypt\n2. Decrypt\n3. Generate Keys")
        mode = get_user_choice(">>> ", {1,2,3})
        print("NOT YET IMPLEMENTED")
    elif cipher_choice == 8:
        handle_freq_analysis()
    restart = input("Would you like to run the program again?:\n1. Re-run\n2. Close Program\n>>> ")
    if restart == "1":
        main()

if __name__ == "__main__":
    print_banner()
    print("Welcome to CipherCrate")
    main()
