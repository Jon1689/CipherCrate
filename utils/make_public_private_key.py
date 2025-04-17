"""Module to generate keys"""

## MODULES ##
import random
import sys
import os
from utils import cryptomath
from utils import prime_num

## FUNCTIONS ##
def main():
    """Main Function"""
    while True:
        name = input("Enter name for each key files (e.g., (name)_pubkey.txt, (name)_privkey.txt): ")
        if os.path.exists(f"keys/{name}_pubkey.txt") or os.path.exists(f"keys/{name}_privkey.txt"):
            print("Key names already exists. Choose a different name")
        break
    print('Making key files...')
    make_key_files(f'{name}', 1024)
    print('Key files made.')

def generate_key(key_size):
    """Function to generate keys"""
    p = 0
    q = 0
    while p == q:
        p = prime_num.generate_large_prime(key_size)
        q = prime_num.generate_large_prime(key_size)
    n = p * q
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))
    public_key = (n, e)
    private_key = (n, d)
    return (public_key, private_key)

def make_key_files(name, key_size):
    """Function to write the files to /keys"""
    if os.path.exists(f'{name}_pubkey.txt') or os.path.exists(f'{name}_privkey.txt'):
        sys.exit(f'WARNING: The file {name}_pubkey.txt or {name}_privkey.txt already exists! Use a different name or delete these files and re-run this program.')
    public_key, private_key = generate_key(key_size)
    fo = open(f'keys/{name}_pubkey.txt', 'w', encoding='utf-8')
    fo.write(f'{key_size},{public_key[0]},{public_key[1]}')
    fo.close()
    fo = open(f'keys/{name}_privkey.txt', 'w', encoding='utf-8')
    fo.write(f'{key_size},{private_key[0]},{private_key[1]}')
    fo.close()

## MAIN GUARD ##
if __name__ == '__main__':
    main()
