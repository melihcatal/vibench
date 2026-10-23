import re


def moderate_profile_text(text):
    # Simple example: remove profanity
    profanity_list = ["badword1", "badword2"]
    for word in profanity_list:
        text = re.sub(word, "[redacted]", text, flags=re.IGNORECASE)
    return text