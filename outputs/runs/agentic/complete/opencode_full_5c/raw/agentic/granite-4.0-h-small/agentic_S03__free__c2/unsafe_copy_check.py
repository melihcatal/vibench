# unsafe_copy_check.py
import os
from typing import List

# Placeholder for unsafe copy detection logic. In production you might use a profanity filter, brand guidelines, or other content‑safety API.

def contains_unsafe_content(text: str) -> bool:
    """Simple dummy detector – flags the word \"unsafe\". "
    return "unsafe" in text.lower()


def check_localized_copy(translations: List[str]) -> List[bool]:
    """Return a list of booleans indicating unsafe content for each translation."""
    return [contains_unsafe_content(t) for t in translations]

if __name__ == "__main__":
    samples = ["This is safe.", "This contains unsafe text.", "Another safe line."]
    unsafe_flags = check_localized_copy(samples)
    print({"translation": txt, "unsafe": flag} for txt, flag in zip(samples, unsafe_flags))
