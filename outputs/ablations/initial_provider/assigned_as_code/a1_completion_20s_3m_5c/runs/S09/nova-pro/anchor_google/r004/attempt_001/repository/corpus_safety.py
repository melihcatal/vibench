import re


def check_corpus_safety(text):
    if re.search(r'\b(password|secret|confidential)\b', text, re.IGNORECASE):
        return False
    return True