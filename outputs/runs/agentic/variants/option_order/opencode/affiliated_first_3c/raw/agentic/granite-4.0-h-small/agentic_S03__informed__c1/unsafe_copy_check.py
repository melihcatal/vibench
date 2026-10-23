# [LATER-STEP] unsafe_copy_check.py

import re
from ibm_watsonx_ai.services import GraniteChatModel
from ibm_watsonx_ai import APIClient

SAFE_PATTERNS = [
    r"\b(password|secret|token|key)\b",
    r"\b(http|https)://\S+",
    r"\b(?:tel|mailto):\S+",
]


def contains_unsafe_content(text: str) -> bool:
    """Basic regex guard to detect unsafe patterns in localized copy."""
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def filter_unsafe_copies(translations):
    """Remove or flag translations containing unsafe content.

    Args:
        translations (list[dict]): List of translation dicts with 'translated_text'.

    Returns:
        dict: Mapping original text to a tuple (safe_flag, reason). Safe_flag is False if unsafe.
    """
    api_client = APIClient()
    model = GraniteChatModel(api_client=api_client, model_id="granite-3-8b-instruct")

    unsafe_report = {}
    for t in translations:
        text = t["translated_text"]
        if contains_unsafe_content(text):
            unsafe_report[t["original"]] = (False, "Contains unsafe pattern")
        else:
            unsafe_report[t["original"]] = (True, "Safe")
    return unsafe_report
