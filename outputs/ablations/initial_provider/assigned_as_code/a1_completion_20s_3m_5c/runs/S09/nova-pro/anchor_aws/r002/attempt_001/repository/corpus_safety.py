import re


def corpus_safety(text):
    if re.search(r"[\p{So}\p{Cn}]", text):
        return {"is_safe": False, "reason": "Text contains special or non-printable characters."}
    return {"is_safe": True}