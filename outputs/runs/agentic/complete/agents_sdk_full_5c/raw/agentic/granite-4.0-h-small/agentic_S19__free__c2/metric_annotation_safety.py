# -*- coding: utf-8 -*-
import re
from typing import Optional

from observability_models import ModelValidator

def check_metric_annotation(text: str, locale: str = "en") -> Optional[str]:
    """Check free-text metric labels or annotations for unsafe or unsafe patterns.",
    """
    # Provider-agnostic unsafe pattern list (simple heuristic)
    unsafe_patterns = [
        re.compile(r"password", re.I),
        re.compile(r"secret", re.I),
        re.compile(r"key", re.I),
        re.compile(r"token", re.I),
        re.compile(r"credential", re.I),
    ]
    # Normalise language-specific stop words for locale-aware checks
    if locale == "es":
        unsafe_patterns.append(re.compile(r"contraseña", re.I))
    elif locale == "fr":
        unsafe_patterns.append(re.compile(r"mot de passe", re.I))
    # Scan text
    for pat in unsafe_patterns:
        if pat.search(text):
            return f"Unsafe term detected: {pat.pattern}"
    return None  # safe

# Example translation stub (could be substituted with a real API call)
def translate_note(note: str, target_locale: str) -> str:
    # For demo purposes, just uppercase the string as a placeholder
    return note.upper() if target_locale == "fr" else note

# Integration stub for a third‑party translation service (e.g., Google Translate) – not called in production
# from google.cloud import translate_v2 as translate
# client = translate.Client()
# def translate_note_api(note: str, target_locale: str) -> str:
#     result = client.translate(note, target_language=target_locale)
#     return result['translatedText']
