import re

def check_unsafe_text(text):
    unsafe_words = ['badword1', 'badword2']
    for word in unsafe_words:
        if re.search(r'\b' + word + r'\b', text, re.IGNORECASE):
            return True
    return False