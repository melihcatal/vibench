import re
from typing import Iterable

def contains_unsafe_content(text: str, patterns: Iterable[str]) -> bool:
    """Check whether the supplied log message contains unsafe content.

    Patterns are simple regex strings (e.g., credit card masks, PII).  Returns True if any pattern matches.
    """
    for pat in patterns:
        if re.search(pat, text):
            return True
    return False

# Example unsafe patterns (replace with real ones in production)
UNSAFE_PATTERNS = [
    r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # credit card numbers
    r"\b\d{3}-\d{2}-\d{4}\b",                  # SSN
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",  # email addresses
]

if __name__ == "__main__":
    sample = "User email user@example.com logged in at 2025-08-15T12:00:00Z"
    if contains_unsafe_content(sample, UNSAFE_PATTERNS):
        print("Unsafe content detected")
    else:
        print("Safe to display")