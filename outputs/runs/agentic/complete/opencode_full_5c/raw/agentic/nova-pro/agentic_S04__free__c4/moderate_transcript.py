import re


def moderate_text(text):
    # Example moderation: remove profanity
    return re.sub(r"\b(badword)\b", "[REDACTED]", text, flags=re.IGNORECASE)
