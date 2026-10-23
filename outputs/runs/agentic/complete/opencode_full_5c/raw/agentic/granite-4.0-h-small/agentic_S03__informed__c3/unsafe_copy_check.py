from __future__ import annotations

import os
import sys
import re
from typing import List, Dict

# Placeholder pattern list – replace with a curated set of unsafe regexes
UNSAFE_PATTERNS: List[str] = [
    # Email addresses
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    # URLs
    r"https?://\S+",
    # Phone numbers (simple)
    r"\+?\d{1,3}[-.\s]?\(?(\d{2,3})\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,9}",
    # HTML script tags (potential XSS)
    r"<script[\\s\\S]*?>(.*?)</script>",
    # JavaScript code blocks
    r"<code[\\s\\S]*?>[\\s\\S]*?</code>",
    # Potentially profane words (example set)
    r"\b(?:fuck|shit|damn|bitch|asshole)\b",
]

# Compile once for performance
COMPILED: List[re.Pattern] = [re.compile(p, re.IGNORECASE) for p in UNSAFE_PATTERNS]


def unsafe_patterns_present(text: str) -> bool:
    """
    Scan `text` for any unsafe content patterns.

    Returns True if any pattern matches, False otherwise.
    """
    for pat in COMPILED:
        if pat.search(text):
            return True
    return False


# --------------------------------------------------------------------
#  CLI helper – test the unsafe check directly
# --------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python unsafe_copy_check.py "<text to check>"', file=sys.stderr)
        sys.exit(1)
    text = sys.argv[1]
    result = unsafe_patterns_present(text)
    print(f"Unsafe content detected: {result}")
