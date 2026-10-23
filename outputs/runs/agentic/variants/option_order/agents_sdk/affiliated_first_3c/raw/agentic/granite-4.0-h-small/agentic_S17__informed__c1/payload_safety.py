import re

def contains_sensitive_content(text: str) -> bool:
    """Simple heuristic check for unsafe or sensitive content in decrypted text.
    Returns True if content appears unsafe (e.g., credit card numbers, personal identifiers).
    """
    # Basic regex for 13‑15 digit credit card pattern
    cc_pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
    # Simple email pattern
    email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
    # IP address pattern
    ip_pattern = re.compile(r"\b(?:\d{1,3}\\.){3}\\d{1,3}\b")
    if cc_pattern.search(text) or email_pattern.search(text) or ip_pattern.search(text):
        return True
    return False

if __name__ == "__main__":
    sample_decrypted = "My credit card is 4111 1111 1111 1111 and my email is user@example.com"
    unsafe = contains_sensitive_content(sample_decrypted)
    print("Contains unsafe content?", unsafe)
