import re


def corpus_safety(text):
    if re.search(r'[a-zA-Z]', text):
        return True
    return False