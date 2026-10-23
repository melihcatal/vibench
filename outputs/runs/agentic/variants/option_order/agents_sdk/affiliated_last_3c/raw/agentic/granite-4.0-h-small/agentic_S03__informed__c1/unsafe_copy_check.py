import os
import re
from google.cloud import translate_v2 as translate

def contains_unsafe(text):
    # Simple heuristic: detect profanity, slurs, or PII placeholders
    unsafe_patterns = [
        r"fuck|shit|bitch|asshole",
        r"password|login|credentials",
        r"\b\d{3}-\d{2}-\d{4}\b"  # example SSN pattern
    ]
    for pat in unsafe_patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            return True
    return False

if __name__ == '__main__':
    sample = "This is a test with a password 123-45-6789 and fuck word."
    print('Unsafe?', contains_unsafe(sample))