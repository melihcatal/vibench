import re


def check_corpus_text(text):
    if re.search(r"\b(hate|violence|discrimination)\b", text, re.IGNORECASE):
        return False
    return True
