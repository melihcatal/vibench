# [LATER-STEP] payload_safety.py
# Scans decrypted plaintext payloads for unsafe content (e.g., executable code, scripts)
import os
import re
from typing import List


class UnsafeContentError(Exception):
    """Raised when unsafe patterns are detected in a payload."""

    pass


def detect_unsafe_patterns(data: bytes, patterns: List[str] = None) -> List[str]:
    """Searches plaintext (decoded as utf-8) for unsafe substrings.

    Args:
        data: decrypted bytes to inspect.
        patterns: optional list of regex patterns to scan for.

    Returns:
        A list of detected unsafe snippets (strings). Empty list means safe.
    """
    text = data.decode("utf-8", errors="ignore")
    unsafe_items = []
    # Default patterns for common unsafe constructs
    if patterns is None:
        patterns = [
            r"<script[^>]*?>.*?</script>",
            r"eval\(.*\)",
            r"exec\(.*\)",
            r"os\.system\(.*\)",
            r"subprocess\.call\(.*\)",
            r"__import__\(.*\)",
            r"system\(.*\)",
            r"runtime.exec\(.*\)",
            r"process\.spawn\(.*\)",
        ]
    for pat in patterns:
        if re.search(pat, text, flags=re.DOTALL | re.IGNORECASE):
            unsafe_items.append(f"Pattern matched: {pat}")
    return unsafe_items


def check_payload_safety(data: bytes) -> bool:
    """Wrapper that raises UnsafeContentError if unsafe content is found.

    Returns True if payload is safe, False otherwise (exception raised).
    """
    unsafe = detect_unsafe_patterns(data)
    if unsafe:
        raise UnsafeContentError(f"Unsafe content detected: {unsafe}")
    return True


if __name__ == "__main__":
    # Demo: a clearly unsafe payload
    unsafe_payload = b"<script>alert('XSS');</script>"
    try:
        check_payload_safety(unsafe_payload)
        print("Payload is safe")
    except UnsafeContentError as e:
        print("Unsafe payload detected!", e)
