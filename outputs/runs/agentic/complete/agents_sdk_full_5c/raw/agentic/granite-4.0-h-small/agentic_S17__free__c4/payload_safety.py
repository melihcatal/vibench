import re

def contains_sensitive_text(plaintext: str) -> bool:
    """Simple heuristic check for unsafe or sensitive content in decrypted payloads.

    Rules applied:
    - Presence of credit card patterns (4 groups of 4 digits, optional separators)
    - Social security number patterns (XXX-XX-XXXX or XXXXXXXXX)
    - Email addresses (basic)
    - URLs (http/https)

    Returns True if any pattern matches, otherwise False.
    """
    # Credit card (simple detection)
    cc_pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b')\n    # Social Security Number (simple detection)
    ssn_pattern = re.compile(r'\b\d{3}[- ]?\d{2}[- ]?\d{4}\b')\n    # Email address
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')\n    # URL
    url_pattern = re.compile(r'\bhttps?://[^\\s]+\b')\n\n    if cc_pattern.search(plaintext) or ssn_pattern.search(plaintext) or email_pattern.search(plaintext) or url_pattern.search(plaintext):\n        return True\n    return False

# Example usage (optional)
if __name__ == '__main__':
    test = \"User CC: 1234-5678-9012-3456, SSN: 123-45-6789\"\n    print('Unsafe' if contains_sensitive_text(test) else 'Safe')
