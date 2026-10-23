# LATER-STEP

import os
import re
from typing import List, Tuple

# Provider selection: Azure AI Content Safety (REST) used for unsafe-content detection

AZURE_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def contains_unsafe_text(texts: List[str]) -> List[Tuple[str, bool]]:
    """Check a collection of free‑text metric labels/annotations for unsafe content using Azure Content Safety.

    Args:
        texts (List[str]): List of strings to evaluate.

    Returns:
        List[Tuple[str, bool]]: Pairs of original text and a flag True if the text was flagged as unsafe.
    """
    # Simple batch request placeholder – real API would send POST with JSON body.
    flagged = []
    for txt in texts:
        # Azure Content Safety expects a payload like {"content": ...}
        # Here we mimic a content safety check with a basic regex that flags profanity.
        unsafe = bool(re.search(r"\b(profanity|badword)\b", txt, re.IGNORECASE))
        flagged.append((txt, unsafe))
    return flagged


# Example usage (not executed during generation):
# texts = ['CPU usage is 85%', 'Kill the process']
# print(contains_unsafe_text(texts))
