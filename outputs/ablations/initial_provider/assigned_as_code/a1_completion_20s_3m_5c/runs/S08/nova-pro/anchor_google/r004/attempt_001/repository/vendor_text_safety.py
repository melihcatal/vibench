import re

def moderate_vendor_text(text: str) -> str:
    # Example moderation: remove any text that contains "fraud" or "scam"
    if re.search(r"\b(fraud|scam)\b", text, re.IGNORECASE):
        return "Moderated text"
    return text