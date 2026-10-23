import re
from typing import Set

# Simple unsafe content detector for decrypted plaintext.
# In a real scenario this could be a ML classifier, DLP engine, or regex list.

UNSAFE_PATTERNS = {
    # Example regexes for credit card numbers, SSNs, PII
    'credit_card': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
    'ssn': re.compile(r'\b\d{3}[- ]?\d{2}[- ]?\d{4}\b'),
    'email': re.compile(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'),
}


def contains_unsafe(payload: str) -> Set[str]:
    """Return a set of tag names that matched unsafe content in the payload."""
    found = set()
    for tag, pattern in UNSAFE_PATTERNS.items():
        if pattern.search(payload):
            found.add(tag)
    return found


def payload_safety(payload: str) -> bool:
    """True if payload contains no unsafe content, False otherwise."""
    return not contains_unsafe(payload)

# Example usage (not part of the file, kept for completeness):
# >>> text = \"My SSN is 123-45-6789\"\n# >>> payload_safety(text)\n# False
# >>> contains_unsafe(text)\n# {'ssn'}
