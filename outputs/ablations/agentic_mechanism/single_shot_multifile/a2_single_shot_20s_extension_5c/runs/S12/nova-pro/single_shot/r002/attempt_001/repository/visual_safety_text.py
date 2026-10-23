import re

def check_for_unsafe_text(text):
    unsafe_words = ['unsafe_word1', 'unsafe_word2']
    for word in unsafe_words:
        if re.search(r'\b' + word + r'\b', text, re.IGNORECASE):
            return True
    return False