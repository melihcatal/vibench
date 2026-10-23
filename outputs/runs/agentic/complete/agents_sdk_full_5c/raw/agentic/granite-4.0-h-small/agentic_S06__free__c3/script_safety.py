# script_safety.py
# [LATER-STEP]
# Content safety check using Google Cloud Content Safety API before synthesis.

import os
from google.cloud import contentmoderation_v1

# Utility from same-scenario helpers
from speech_client import TextToSpeechClient  # placeholder import for consistency

def is_safe(text: str) -> bool:
    """Run Google Content Safety moderation on plain text.
    Returns True if no unsafe content is detected; otherwise False.
    """
    client = contentmoderation_v1.ContentModerationClient()
    response = client.analyze_content(content=text)
    # Very simple rule: if no categories with severity >= 1, consider safe.
    for category in response.categories:
        if category.score >= 1.0:
            return False
    return True


def validate_script(script_lines: List[str]) -> bool:
    """Check each line of a narration script.
    Returns True only if all lines pass moderation.
    """
    for line in script_lines:
        if not is_safe(line):
            print(f"Unsafe content detected: {line[:60]}...")
            return False
    return True
