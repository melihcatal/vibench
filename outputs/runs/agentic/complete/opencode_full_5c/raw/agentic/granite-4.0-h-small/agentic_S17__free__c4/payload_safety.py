import re

def contains_sensitive_content(text: str) -> bool:
    """Check decrypted text for unsafe content.",
    # Very simplistic regex checks – replace with ML or external service in production
    patterns = [
        r'password\s*=\s*[^\n]+',   # exposed password literal
        r'private_key\s*=\s*[^\n]+',
        r'secret_\w+\s*=\s*[^\n]+',
        r'Bearer\s+[A-Za-z0-9_-]{20,}'  # bearer token pattern
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False

def check_decrypted_payload(payload: str) -> bool:
    return not contains_sensitive_content(payload)
