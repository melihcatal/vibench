# later-step implementation - safety filter for narration scripts

import re
from typing import List

# Simple unsafe-content check (placeholder - in real usage integrate with a moderation service)

UNSAFE_PATTERNS: List[str] = [
    r"\b(?:hate|violence|sexual|drugs)\b",
    r"\b(?:kill|murder|shoot)\b",
]


async def is_script_safe(script: str) -> bool:
    """Return True if the script passes basic safety checks."""
    lowered = script.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, lowered):
            return False
    return True


async def filter_unsafe_scripts(scripts: List[str]) -> List[str]:
    """Filter out unsafe scripts and return a list of safe ones."""
    safe = []
    for s in scripts:
        if await is_script_safe(s):
            safe.append(s)
    return safe
