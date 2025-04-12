# Jon Greko
# 15 Jan 2025

def main():
    plaintext = input("Enter message to encrypt/decrypt using Reverse Cipher: ")
    cipher_text = reverse_cipher(plaintext)
    print(cipher_text)

def reverse_cipher(message):
    ciphertext = ""
    i = len(message) - 1

    while i >= 0:
        ciphertext = ciphertext + message[i]
        i -= 1
    return ciphertext

if __name__ == "__main__":
    main()
