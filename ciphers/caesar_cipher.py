# Caesar Cipher

from utils.file_loader import load_dictionary

## CONSTANTS ##
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.,'
WORDS = load_dictionary()

## FUNCTIONS ##
def main():
    """Main Function"""
    print("This program encrypts or decrypts messages using the Caesar Cipher.")
    
    while True:
        mode = input("Enter (E)ncrypt, (D)ecrypt, or (H)ack: ").upper().strip()
        if mode in ("E", "D", "H"):
            break    
        print("\33[31mInvalid input. Please enter 'E', 'D', or 'H'.\33[0m")

    if mode == "H":
        message = input("Enter the encrypted message to hack: ")
        translation, key = caesar_hacker(message)
        print(f"Best Guess (key={key}: {translation})")
        return

    message = input("Enter your message: ")

    while True:
        try:
            key = int(input("Enter a key (1-26): "))
            if 1 <= key <= 26:
                break
            else:
                print("\033[31mKey must be between 1 and 26.\033[0m")
        except ValueError:
            print("\033[31mPlease enter a valid integer.\033[0m")

    result = caesar_cipher(message, key, mode)
    print(f"\nTranslated message: {result}")

def caesar_cipher(message, key, mode):
    """
    Caesar Cipher Function
    1. Takes message, key, and mode as input.
    2. Returns the translated text.
    """
    translated = ""
    for char in message:
        if char in SYMBOLS:
            translated_index = SYMBOLS.find(char)
            if mode == "E":
                translated_index = (translated_index + key) % len(SYMBOLS)
            elif mode == "D":
                translated_index = (translated_index - key) % len(SYMBOLS)
            translated += SYMBOLS[translated_index]
        else:
            translated += char
    return translated

def caesar_hacker(message):
    best_key = 0
    best_translation = ""
    best_score = 0

    for key in range(1, 27):
        translated = caesar_cipher(message, key, "D")
        words = translated.split()
        matches = sum(1 for word in words if word.lower() in WORDS)

        if matches > best_score:
            best_score = matches
            best_key = key
            best_translation = translated
    return (best_translation, best_key) if best_score > 0 else "---COULDN'T HACK MESSAGE---"

if __name__ == "__main__":
    main()
