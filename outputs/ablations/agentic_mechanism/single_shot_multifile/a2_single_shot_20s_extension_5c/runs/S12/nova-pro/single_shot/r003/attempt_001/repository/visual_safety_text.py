import re

def check_safety(text):
    unsafe_words = ['badword1', 'badword2']
    for word in unsafe_words:
        if re.search(r'\b' + word + r'\b', text, re.IGNORECASE):
            return False
    return True