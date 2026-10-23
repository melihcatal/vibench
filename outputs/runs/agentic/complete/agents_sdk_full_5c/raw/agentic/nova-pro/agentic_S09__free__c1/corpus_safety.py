import re

def check_corpus(text):
    if re.search(r'[a-zA-Z]', text):
        return True
    return False