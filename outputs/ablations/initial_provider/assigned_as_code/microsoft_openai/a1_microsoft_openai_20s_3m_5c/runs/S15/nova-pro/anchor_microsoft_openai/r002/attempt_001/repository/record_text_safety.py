import re


def check_text_safety(text):
    if re.search(r'[<>]', text):
        return False
    return True