# unsafe_copy_check.py
import re
from typing import List
from translation_models import TranslateResponse


def unsafe_patterns() -> List[str]:
    """Return a list of regex patterns considered unsafe in localized copy."""
    return [
        r"(password|passwd)\\s*=\\s*\\w+",
        r"(secret|api_key)\\s*=\\s*\\w+",
        r"(ccnum|creditcard)\\s*[:=]\\s*\\d{13,16}",
    ]


def unsafe_copy_check(
    translation_results: List[TranslateResponse], source_texts: List[str]
) -> List[str]:
    """Check translated texts for unsafe patterns and return list of problematic translations."""
    unsafe_regexes = unsafe_patterns()
    unsafe = []
    for i, trans in enumerate(translation_results):
        text = trans["translated_text"]
        for pat in unsafe_regexes:
            if re.search(pat, text):
                unsafe.append(f"Issue in entry {i}: {text}")
                break
    return unsafe
