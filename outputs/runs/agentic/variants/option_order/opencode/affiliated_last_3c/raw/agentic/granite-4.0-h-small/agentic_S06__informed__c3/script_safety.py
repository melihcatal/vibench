import os
import json
import re
from typing import List

# Simple unsafe content detection - checks for profanity and hate speech keywords.
# In production replace with Perspective API or Amazon Comprehend call.
UNSAFE_WORDS = [
    "hate",
    "kill",
    "attack",
    "bomb",
    "terror",
    "racial slur",
    "sexist",
    "offensive",
]


def contains_unsafe(content: str) -> bool:
    """Return True if any unsafe word or pattern is found."""
    lowered = content.lower()
    for word in UNSAFE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            return True
    return False


def check_script(file_path: str) -> List[str]:
    """Read a narration script file and return list of lines flagged as unsafe."""
    flagged = []
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if contains_unsafe(line):
                flagged.append(f"Line {i}: {line.strip()}")
    return flagged
