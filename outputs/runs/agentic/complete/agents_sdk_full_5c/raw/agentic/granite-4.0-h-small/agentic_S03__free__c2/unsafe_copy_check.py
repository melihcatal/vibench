# unsafe_copy_check.py
import re

def contains_unsafe_content(text: str) -> bool:
    """Heuristic check for unsafe copy (profanity, personal data, etc.).
    This is a very simple regex based detector; replace with a real service in production.
    """
    # Detect emails
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        return True
    # Detect IPs
    if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text):
        return True
    # Detect URLs
    if re.search(r"\bhttps?://\S+\b", text):
        return True
    # Detect profanity (simple list)
    profanity = re.compile(r"\b(badword|curse)\b", re.IGNORECASE)
    if profanity.search(text):
        return True
    return False
