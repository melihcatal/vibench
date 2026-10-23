# [LATER-STEP] unsafe_copy_check.py
"""Check localized copy for unsafe content after translation.
Runs simple pattern matching to flag profanity, hate speech, or PII that may have been introduced by translation."

from __future__ import annotations
import re
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Unsafe content patterns (extend as needed)
# ---------------------------------------------------------------------------
PROFANITY_PATTERNS = [
    r"\b(badword1|badword2)\b",  # placeholder examples
]
PII_PATTERNS = [
    # Emails
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    # Phone numbers (simple US style)
    r"\b\+?\d{1,3}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{4}\b",
    # Generic placeholders that look like variables
    r"\{[^\}]+\}",
]

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

_ORIGINAL_TEXT_KEY = "source_text"
_TRANSLATED_TEXT_KEY = "translated_text"


def _contains_unsafe(text: str) -> bool:
    """Return True if any pattern matches the provided text."
    """
    lowered = text.lower()
    for prof in PROFANITY_PATPATTERNS:
        if re.search(prof, lowered):
            return True
    for pii in PII_PATTERNS:
        if re.search(pii, lowered):
            return True
    return False


def check_unsafe(translated_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a list of segments flagged as unsafe.

    Each segment dict should contain at least the keys:
        source_text, translated_text
    """
    unsafe = []
    for seg in translated_segments:
        # Only inspect translated copy
        if _contains_unsafe(seg.get(_TRANSLATED_TEXT_KEY, "")):
            unsafe.append(seg)
    return unsafe

# ---------------------------------------------------------------------------
# CLI helper (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, json, sys
    parser = argparse.ArgumentParser(description="Scan translated segments for unsafe content.")
    parser.add_argument("input_file", type=str, help="Path to JSON file with list of segment dicts.")
    args = parser.parse_args()
    with open(args.input_file) as f:
        segments = json.load(f)
    unsafe_list = check_unsafe(segments)
    if unsafe_list:
        print("Unsafe segments detected:", file=sys.stderr)
        print(json.dumps(unsafe_list, indent=2), file=sys.stderr)
    else:
        print("No unsafe content found.", file=sys.stderr)
