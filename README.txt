# 🔐 CipherCrate

CipherCrate is a Python-based cipher suite that includes multiple encryption and decryption algorithms. It supports common ciphers such as Caesar, Vigenère, Affine, Transposition, and Simple Substitution, along with tools for cryptanalysis (hacking) using dictionary-based methods. The project is designed to demonstrate various cryptography techniques and provides a framework for learning and experimentation.

---

## 📦 Features

- **Caesar Cipher**: A simple substitution cipher where each letter in the plaintext is shifted by a specified number.
- **Vigenère Cipher**: A more complex cipher that uses a keyword to shift each letter of the plaintext in a cyclical manner.
- **Transposition Cipher**: Encrypts by rearranging the letters in a specific pattern.
- **Affine Cipher**: A substitution cipher based on mathematical functions.
- **Simple Substitution Cipher**: A cipher where each letter is substituted with another letter based on a fixed mapping.
- **Cryptanalysis**: Includes basic hacking functionality for certain ciphers using dictionary-based methods.

---

## 🗂️ Project Structure

CipherCrate/
│
├── main.py
├── requirements.txt
├── README.md
│
├── dictionary/
│   └── dictionary.txt
│
├── ciphers/
|   ├── __init__.py
│   ├── reverse_cipher.py
│   ├── caesar_cipher.py
│   ├── transposition_cipher.py
│   ├── affine_cipher.py
│   ├── simple_sub.py
│   └── vigenere_cipher.py
│
└── utils/
    ├── __init__.py
    ├── detect_english.py 
    ├── file_loader.py
    └── frequency_analysis.py

---

## 📥 Installation

To use CipherCrate, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/CipherCrate.git
cd CipherCrate
pip install -r requirements.txt
