import re


def check_script_safety(script):
    unsafe_words = ["badword1", "badword2"]
    for word in unsafe_words:
        if re.search(word, script, re.IGNORECASE):
            return False
    return True
