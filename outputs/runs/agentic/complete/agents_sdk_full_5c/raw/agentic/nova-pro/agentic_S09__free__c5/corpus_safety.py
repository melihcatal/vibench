import re

def check_corpus(text):
    if re.search(r'[\W_]+', text):
        return False
    return True
