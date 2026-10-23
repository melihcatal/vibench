import re


def moderate_vendor_text(text):
    if re.search(r"\b(fraud|scam|phishing)\b", text, re.IGNORECASE):
        return "Text contains sensitive content"
    return text