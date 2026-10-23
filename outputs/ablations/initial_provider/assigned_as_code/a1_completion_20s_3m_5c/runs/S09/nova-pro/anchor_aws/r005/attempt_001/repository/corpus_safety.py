import re


def check_corpus_text(text):
    if re.search(r"[^a-zA-Z0-9\s]", text):
        return False
    return True