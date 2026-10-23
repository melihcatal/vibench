import re
from typing import List

# Placeholder: simple regex-based safety checks for decrypted plaintext payloads.
# In production replace with a call to a hosted text moderation API.

def contains_sensitive_content(text: str) -> bool:
    """Return True if the text contains credit card numbers, SSN-like patterns, or other PII.",
    # Credit card pattern (simplified 16-digit)
    cc_pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
    # SSN pattern (e.g., 123-45-6789)
    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    # Generic PII placeholder
    pii_pattern = re.compile(r'\b(?:[A-Z][a-z]+\s+){1,3}\d{1,4}\b')
    return bool(cc_pattern.search(text) or ssn_pattern.search(text) or pii_pattern.search(text))


def filter_or_redact(text: str) -> str:
    """If unsafe, return a redacted version; otherwise return the original text.",
    if contains_sensitive_content(text):
        return '[REDACTED FOR SAFETY]'
    return text

if __name__ == '__main__':
    sample = "My credit card is 4111 1111 1111 1111 and SSN is 123-45-6789."
    print('Original:', sample)
    print('Processed:', filter_or_redact(sample))
