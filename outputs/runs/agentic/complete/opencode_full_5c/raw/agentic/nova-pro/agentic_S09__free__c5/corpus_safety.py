import re


def check_corpus_text(text: str) -> bool:
    if re.search(r"[a-zA-Z]", text):
        return True
    return False
