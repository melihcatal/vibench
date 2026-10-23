from typing import Optional

def normalize_language_code(lang: Optional[str]) -> Optional[str]:
    if lang is None:
        return None
    return lang.upper().strip()
