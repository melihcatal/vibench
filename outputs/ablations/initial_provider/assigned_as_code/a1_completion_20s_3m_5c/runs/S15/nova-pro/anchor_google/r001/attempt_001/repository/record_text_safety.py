import re

def check_text_safety(text):
    if re.search(r'[\W_]+', text):
        return False
    return True