"""Frequency Analyzer"""

## CONSTANTS ##

ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ" # Sets the constant ETAOIN
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Sets the constant LETTERS

## FUNCTIONS ##

def get_letter_count(message):
    """Grabs the letter cound of each letter in the message"""
    letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
            'K': 0, 'L': 0, 'M': 0,'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
            'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for letter in message.upper():
        if letter in LETTERS:
            letter_count[letter] += 1
    return letter_count

def get_item_at_index_zero(items):
    """Helper function to grab the get the index of 0"""
    return items[0]

def get_frequency_order(message):
    """Returns the freq order or each letter in the mssage"""
    letter_to_freq = get_letter_count(message)
    freq_to_letter = {}
    for letter in LETTERS:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)
    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=ETAOIN.find, reverse=True)
        freq_to_letter[freq] = "".join(freq_to_letter[freq])
    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=get_item_at_index_zero, reverse=True)
    freq_order = []
    for freq_pair in freq_pairs:
        freq_order.append(freq_pair[1])
    return "".join(freq_order)

def english_freq_match_score(message):
    """Gets the match score"""
    freq_order = get_frequency_order(message)
    match_score = 0
    for common_letter in ETAOIN[:6]:
        if common_letter in freq_order[:6]:
            match_score += 1
    for uncommon_letter in ETAOIN[-6:]:
        if uncommon_letter in ETAOIN[-6:]:
            match_score += 1
    return match_score
