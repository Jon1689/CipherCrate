"""CipherCrate Main Program"""

## MODULES ##
from random import randint
import sys
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
# Used for coloring text in terminal
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = "\033[38;5;208m"
TEAL = "\033[36m"
MAGENTA = "\u001b[35m"
RESET = '\033[0m'

## FUNCTIONS ##
def print_banner():
    """Prints Program Banner"""
    print(rf"""{ORANGE}
#########################################################
#{RESET}  ____ _       _                ____           _       {ORANGE}#
#{RESET} / ___(_)_ __ | |__   ___ _ __ / ___|_ __ __ _| |_ ___ {ORANGE}#
#{RESET}| |   | | '_ \| '_ \ / _ \ '__| |   | '__/ _` | __/ _ \{ORANGE}#
#{RESET}| |___| | |_) | | | |  __/ |  | |___| | | (_| | ||  __/{ORANGE}#
#{RESET} \____|_| .__/|_| |_|\___|_|   \____|_|  \__,_|\__\___|{ORANGE}#
#{RESET}        |_|                                            {ORANGE}#
#########################################################
{RESET}""")

def get_cipher_name(cipher_choice):
    """Returns a string of the cipher name"""
    if cipher_choice == 2:
        return f"\n{ORANGE}--###--Caesar Cipher--###--{RESET}"
    elif cipher_choice == 3:
        return f"\n{ORANGE}--###--Transposition Cipher--###--{RESET}"
    elif cipher_choice == 4:
        return f"\n{ORANGE}--###--Affine Cipher--###--{RESET}"
    elif cipher_choice == 5:
        return f"\n{ORANGE}--###--Simple Substitution Cipher--###--{RESET}"
    elif cipher_choice == 6:
        return f"\n{ORANGE}--###--Vigenere Cipher--###--{RESET}"
    elif cipher_choice == 7:
        return f"\n{ORANGE}--###--Public Key Cipher--###--{RESET}"
    elif cipher_choice == 8:
        return f"\n{ORANGE}--###--Frequency Analyzer--###--{RESET}"
    elif cipher_choice == 1:
        return f"\n{ORANGE}--###--Reverse Cipher--###--{RESET}"

def get_user_choice(prompt, options):
    """Function for validating menu input"""
    while True:
        choice = input(prompt)
        if choice.isdigit() and int(choice) in options:
            return int(choice)
        print(f"{RED}Invalid choice. Please try again.{RESET}")

def get_encryption_key(cipher_choice, message):
    """Gets Encryption Key"""
    print(f"\n{ORANGE}Key Type:{RESET}")
    print(f"""
        {ORANGE}[{RESET}1{ORANGE}] Random{RESET}
        {ORANGE}[{RESET}2{ORANGE}] Personal{RESET}
        """)
    key_type = get_user_choice(f"{TEAL}>>> ", {1,2})
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
                key = input(f"{RESET}Enter a number between 1-26:\n{TEAL}>>> ")
                if key.isdigit() and 1 <= int(key) <= 26:
                    return int(key)
                print(f"{RED}Invalid key. Must be a number from 1 to 26.{RESET}")
        elif cipher_choice == 3: #Transposition Cipher Personal KEy
            while True:
                key = input(f"{RESET}Enter a number between 2 and {(len(message) // 2)}:\n{TEAL}>>> ")
                if key.isdigit() and 1 < int(key) <= (len(message) // 2):
                    return int(key)
                print(f"{RED}Invalid key. Must be a number from 2 to {len(message) // 2}.{RESET}")
        elif cipher_choice == 4: #Affine Cipher Personal Key
            while True:
                key_input = input(f"{RESET}Enter a numeric key (will be split into A and B):\n{TEAL}>>> ")
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
                key_input = input(f"{RESET}Enter a alphabetic key:\n{TEAL}>>> ")
                if key_is_valid(key_input):
                    return key_input.upper()
                else:
                    print(f"{RED}Please enter a proper key. Must include all 26 letters of the alphabet.{RESET}")
        elif cipher_choice == 6: #Vigenere Cipher Personal Key
            while True:
                key = input(f"{RESET}Enter the key you would like to use here:\n{TEAL}>>> ")
                if key.isalpha() and len(key) < len(message):
                    break
                else:
                    print(f"{RED}Please only choose a word with no numbers and shorter than the message.{RESET}")
            return key.upper()

def handle_caesar(mode):
    """Runs Caesar Cipher"""
    message = input(f"{RESET}Enter your message:\n{TEAL}>>> ")
    # Get encryption key if the user wants to encrypt or decrypt
    key = get_encryption_key(2, message) if mode in (1,2) else None
    if mode == 3: # Hack Mode
        output, key = caesar_hacker(message)
    else: # Encrypt/Decrypt Mode
        cipher_mode = "E" if mode == 1 else "D"
        output = caesar_cipher(message, key, cipher_mode)
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD--###--{RESET}")
    copy(output)
    print(f"{ORANGE}KEY USED: {GREEN}{key}{RESET}")

def handle_reverse():
    """Runs Reverse Cipher"""
    message = input(f"{RESET}Enter your message:\n{TEAL}>>> ")
    output = reverse_cipher(message)
    copy(output)
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD-###-{RESET}")

def handle_transposition(mode):  #TODO: Fix case sensitivity
    """Runs Transposition Cipher"""
    message = input(f"{RESET}Enter your message here:\n{TEAL}>>> ")
    # Get encryption key if the user wants to encrypt or decrypt
    key = get_encryption_key(3, message) if mode in range(1,3) else None
    output = ""
    if mode == 3: # Hack Mode
        output, key = transpo_hack(message)
    elif mode == 1: # Encrypt Mode
        output = transpo_encrypt(message, key)
    elif mode == 2: # Decrypt Mode
        output = transpo_decrypt(message, key)
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD-###-{RESET}")
    copy(output)
    print(f"{ORANGE}KEY USED: {GREEN}{key}{RESET}")

def handle_affine(mode):
    """Runs Affine Cipher"""
    message = input(f"{RESET}Enter your message here:\n{TEAL}>>> ")
    # Get encryption key if the user wants to encrypt or decrypt
    key = get_encryption_key(4, message) if mode in range(1,3) else None
    if mode == 3: # Hack Mode
        output, key = affine_hack(message)
    elif mode == 1: # Encrypt Mode
        output = affine_encrypt(message, key)
    elif mode == 2: # Decrypt Mode
        output = affine_decrypt(message, key)
    else:
        print(f"{RED}Invalid mode selected{RESET}")
        return
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD-###--{RESET}")
    copy(output)
    print(f"{ORANGE}KEY USED: {GREEN}{key}{RESET}")

def handle_simple(mode):
    """Runs Simple Substitution Cipher"""
    if mode == 3: # Hack Mode
        message = input(f"{RESET}Enter your encrypted message to hack:\n{TEAL}>>> ")
        mapping = hack_simple(message)
        decrypted = decrypt_with_cipherletter_mapping(message, mapping)
        print(f"{GREEN}{decrypted}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD--###--{RESET}")
        copy(decrypted)
        return
    message = input(f"{RESET}Enter your message here:\n{TEAL}>>> ")
    key = get_encryption_key(5, message)
    mode_str = "encrypt" if mode == 1 else "decrypt"
    output = simple_substitution(message, key, mode_str)
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD--###--{RESET}")
    copy(output)
    if mode in (1,2):
        print(f"{ORANGE}KEY USED: {GREEN}{key}{RESET}")

def handle_vigenere(mode):
    """Runs Vigenere Cipher"""
    if mode == 3: # Hack Mode
        message = input(f"{RESET}Enter your encrypted message to hack:\n{TEAL}>>> ")
        decrypted, key = hack_vigenere(message)
        print(f"{GREEN}{decrypted}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD--###--{RESET}")
        copy(decrypted)
        return
    message = input(f"{RESET}Enter your message here:\n{TEAL}>>> ")
    key = get_encryption_key(6, message)
    output = ""
    if mode == 1: # Encrypt Mode
        output = vigenere_encrypt(message, key)
    elif mode == 2: # Decrypt Mode
        output = vigenere_decrypt(message, key)
    print(f"{GREEN}{output}{RESET}\n{MAGENTA}--###--COPIED TO CLIPBOARD--###--{RESET}")
    copy(output)
    print(f"{ORANGE}KEY USED: {GREEN}{key}{RESET}")

def handle_freq_analysis():
    """Runs Frequency Analysis"""
    message = input(f"{RESET}Please input english sentence to analyze here:\n{TEAL}>>> ")
    match_score = english_freq_match_score(message)
    letter_count = get_letter_count(message)
    freq_order = get_frequency_order(message)
    print(f"{RESET}The frequency order of your sentense is: {GREEN}{freq_order}{RESET}")
    # Does not print letters with a count of 0
    for key, value in letter_count.items():
        if value == 0:
            continue
        print(f"{RESET}Letter: {GREEN}{key}{RESET} | Frequency: {GREEN}{value}{RESET}")
    print(f"{RESET}Your match score is {GREEN}{match_score}{RESET}.")

def main():
    """MAIN FUNCTION"""
    # Main Menu
    print(f"{ORANGE}Choose a cipher:")
    print(f"""
        [{RESET}1{ORANGE}] Reverse Cipher
        [{RESET}2{ORANGE}] Caesar Cipher
        [{RESET}3{ORANGE}] Transpositional Cipher
        [{RESET}4{ORANGE}] Affine Cipher
        [{RESET}5{ORANGE}] Simple Substitution Cipher
        [{RESET}6{ORANGE}] Vigenere Cipher
        [{RESET}7{ORANGE}] Public Key Cipher
        [{RESET}8{ORANGE}] Frequency Analysis{RESET}
        """)
    cipher_choice = get_user_choice(f"{TEAL}>>> ", range(1,9))
    mode = None
    if cipher_choice == 1: # Reverse Cipher
        print(get_cipher_name(cipher_choice))
        handle_reverse()
    elif cipher_choice in range(2,7): # All other ciphers
        print(get_cipher_name(cipher_choice))
        print(f"\n{ORANGE}Select Mode:")
        print(f"""
            [{RESET}1{ORANGE}] Encrypt
            [{RESET}2{ORANGE}] Decrypt
            [{RESET}3{ORANGE}] Hack
            """)
        mode = get_user_choice(f"{TEAL}>>> ", {1,2,3})
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
    elif cipher_choice == 7: # Public Key Cipher
        print(f"{ORANGE}Select Mode:\n[{RESET}1{ORANGE}] Encrypt\n[{RESET}2{ORANGE}] Decrypt\n[{RESET}3{ORANGE}] Generate Keys")
        mode = get_user_choice(f"{TEAL}>>> ", {1,2,3})
        print("NOT YET IMPLEMENTED")
    elif cipher_choice == 8: # Frequency Analysis
        handle_freq_analysis()
    # Return to Main Menu Option
    print(f"\n{ORANGE}Re-Run Program?")
    print(f"""
        [{RESET}1{ORANGE}] Re-Run
        [{RESET}2{ORANGE}] Close Program
        """)
    while True:
        restart = input(f"{TEAL}>>> ")
        if restart in ("1", "2"):
            break
        print(f"{RED}Invalid choice. Please try again.{RESET}")
    print(f"{RESET}")
    if restart == "1":
        main()
    elif restart == "2":
        print(f"{ORANGE}Goodbye!\n{RESET}")
        sys.exit()

if __name__ == "__main__":
    print_banner()
    main()
