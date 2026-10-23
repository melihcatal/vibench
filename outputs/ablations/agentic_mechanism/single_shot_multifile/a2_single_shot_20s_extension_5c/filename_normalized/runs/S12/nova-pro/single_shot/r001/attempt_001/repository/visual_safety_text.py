import re

def visual_safety_text(text):
    unsafe_words = ['badword1', 'badword2']
    for word in unsafe_words:
        if re.search(r'\b' + word + r'\b', text, re.IGNORECASE):
            return False
    return True