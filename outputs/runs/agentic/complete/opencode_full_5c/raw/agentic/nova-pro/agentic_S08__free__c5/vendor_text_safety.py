import re


def moderate_text(text):
    moderated_text = re.sub(r"\bbadword\b", "[REDACTED]", text, flags=re.IGNORECASE)
    return moderated_text
