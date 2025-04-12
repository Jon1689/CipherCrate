"""File Loader"""
import os

def load_dictionary():
    """Load the dictionary file and return a list of lowercase words."""
    dict_path = os.path.join(os.path.dirname(__file__), '..', 'dictionary', 'dictionary.txt')
    dict_path = os.path.abspath(dict_path)
    with open(dict_path, encoding="utf-8") as dictionary_file:
        return [word.strip().lower() for word in dictionary_file]
