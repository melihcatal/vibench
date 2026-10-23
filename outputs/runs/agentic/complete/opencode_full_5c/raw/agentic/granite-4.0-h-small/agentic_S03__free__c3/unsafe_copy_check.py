import re
from typing import List

PROVIDER_NAME = "deepl"

# Simple unsafe content patterns (example regexes)
UNSAFE_PATTERNS = [
    r"\b(violent|explicit sexual|hate speech)\b",
    r"\b(drug|weapon|alcohol abuse)\b",
]


async def unsafe_copy_check(translations: List[str]) -> List[bool]:
    """Check localized copy for unsafe content.",
    Returns a list of booleans aligned with the input translations,
    each True if the translation contains any unsafe pattern.
    """
    results = []
    for text in translations:
        unsafe = any(re.search(p, text, re.IGNORECASE) for p in UNSAFE_PATTERNS)
        results.append(unsafe)
    return results
