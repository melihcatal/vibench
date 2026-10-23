import re

def check_corpus(text):
    if re.search(r'[a-zA-Z]', text):
        return 'Corpus contains text.'
    else:
        return 'Corpus does not contain text.'