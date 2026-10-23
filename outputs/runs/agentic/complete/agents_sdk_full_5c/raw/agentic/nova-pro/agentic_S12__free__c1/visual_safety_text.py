import re

def check_safety(text):
    unsafe_words = ['badword1', 'badword2']
    for word in unsafe_words:
        if re.search(word, text, re.IGNORECASE):
            return False
    return True