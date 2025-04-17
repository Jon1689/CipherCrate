"""Module to encrypt and decrypt messages using public key cryptography"""

## MODULES ##
import sys
import math
import os

## CONSTANTS ##
SYMBOLS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 '
            '!?.@#$%^&*()-_=+[]}{|;:",—’<>/~`\\\'')

## FUNCTIONS ##
def main():
    """Main Function"""
    while True:
        filename = input("Enter the name to save to or read from the encrypted file (e.g., example_encrypted.txt): ")
        if filename == '':
            print("Please enter a valid file name ending with .txt")
        elif not filename.endswith('.txt'):
            print("Please enter a valid file name ending with .txt")
        else:
            break
    while True:
        mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ").lower()
        if mode in ['encrypt', 'decrypt']:
            break
        else:
            print("Please enter either 'encrypt' or 'decrypt'.")
    if mode == 'encrypt':
        message = input('Enter the message to encrypt: ')
        while True:
            public_key_filename = input('Enter the public key filename (e.g., al_sweigart_pubkey.txt): ') 
            if os.path.exists(f"keys/{public_key_filename}"):
                break
            else:
                print("Public key file not found. Please enter a valid file name.")
        print(f'Encrypting and writing to {filename}...')
        encrypted_text = encrypt_and_write_to_file(filename, public_key_filename, message)
        print('Encrypted text:')
        print(encrypted_text)
    elif mode == 'decrypt':
        while True:
            priv_key_filename = input('Enter the private key filename (e.g., al_sweigart_privkey.txt): ')
            if os.path.exists(f"keys/{priv_key_filename}"):
                break
            else:
                print("Private key file not found. Please enter a valid file name.")
        print(f'Reading from {filename} and decrypting...')
        decrypted_text = read_from_file_and_decrypt(filename, priv_key_filename)
        print('Decrypted text:')
        print(decrypted_text)

def get_blocks_from_text(message, block_size):
    """Convert the text message into blocks of integers."""
    for character in message:
        if character not in SYMBOLS:
            print(f'ERROR: The symbol set does not have the character {character}')
            sys.exit()
    block_ints = []
    for block_start in range(0, len(message), block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(message))):
            block_int += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % block_size))
        block_ints.append(block_int)
    return block_ints

def get_text_from_blocks(block_ints, message_length, block_size):
    """Convert the block integers back to text."""
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                char_index = block_int // (len(SYMBOLS) ** i)
                block_int = block_int % (len(SYMBOLS) ** i)
                block_message.insert(0, SYMBOLS[char_index])
        message.extend(block_message)
    return ''.join(message)

def encrypt_message(message, key, block_size):
    """Encrypt the message using the public key."""
    encrypted_blocks = []
    n, e = key
    for block in get_blocks_from_text(message, block_size):
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks

def decrypt_message(encrypted_blocks, message_length, key, block_size):
    """Decrypt the message using the private key."""
    decrypted_blocks = []
    n, d = key
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)

def read_key_file(key_filename):
    """Read the key file and return the key size, n, and e or d."""
    fo = open(f"keys/{key_filename}", encoding='utf-8')
    content = fo.read()
    fo.close()
    key_size, n, e_or_d = content.split(',')
    return (int(key_size), int(n), int(e_or_d))

def encrypt_and_write_to_file(message_filename, key_filename, message, block_size=None):
    """Encrypt the message and write it to the file."""
    key_size, n, e = read_key_file(key_filename)
    if block_size is None:
        block_size = int(math.log(2 ** key_size, len(SYMBOLS)))
    if not math.log(2 ** key_size, len(SYMBOLS)) >= block_size:
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
    encrypted_blocks = encrypt_message(message, (n, e), block_size)
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ','.join(encrypted_blocks)
    encrypted_content = f'{len(message)}_{block_size}_{encrypted_content}'
    fo = open(f"encryptions/{message_filename}", 'w', encoding='utf-8')
    fo.write(encrypted_content)
    fo.close()
    return encrypted_content

def read_from_file_and_decrypt(message_filename, key_filename):
    """Read the encrypted file and decrypt it using the private key."""
    key_size, n, d = read_key_file(key_filename)
    fo = open(f"encryptions/{message_filename}", encoding='utf-8')
    content = fo.read()
    message_length, block_size, encrypted_message = content.split('_')
    message_length = int(message_length)
    block_size = int(block_size)
    if block_size < 1 or not math.log(2 ** key_size, len(SYMBOLS)) >= block_size:
        sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
    encrypted_blocks = []
    try:
        encrypted_blocks = [int(block) for block in encrypted_message.split(',')]
    except ValueError:
        sys.exit("ERROR: Encrypted message contains invalid blocks.")
    return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)

## MAIN GUARD ##
if __name__ == '__main__':
    main()