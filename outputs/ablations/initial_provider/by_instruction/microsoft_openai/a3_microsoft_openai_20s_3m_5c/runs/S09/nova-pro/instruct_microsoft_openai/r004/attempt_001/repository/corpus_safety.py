import re

def corpus_safety(text: str):
    if re.search(r'[^a-zA-Z0-9\s]', text):
        return False
    return True