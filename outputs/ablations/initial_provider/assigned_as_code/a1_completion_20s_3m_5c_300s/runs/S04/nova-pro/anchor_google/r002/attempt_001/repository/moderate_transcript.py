import re


def moderate_transcript(text):
    # Example moderation: remove profanity
    profanity = ["badword1", "badword2"]
    for word in profanity:
        text = re.sub(r"\b" + word + r"\b", "[REDACTED]", text, flags=re.IGNORECASE)
    return text