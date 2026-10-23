"""
Flag or redact unsafe spans from text based on Azure AI Content Safety analysis.
Provider: Azure AI Content Safety via azure-ai-contentsafety SDK.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from safety_client import get_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    parse_azure_response,
    SafetyCategory,
    SafetySeverity,
    CategoryScore,
)
from azure.core.exceptions import HttpResponseError
from typing import Optional, List, Dict
import re


def _build_category_regex_flags() -> Dict[SafetyCategory, List[str]]:
    """Build simple keyword flag lists for unsafe category detection in text spans."""
    flags = {
        SafetyCategory.HATE: [
            r"\b(hate|hated|slur|discriminat|bigot|racist|sexist)\b",
            r"\b(superior|inferior|subhuman|vermin)\b",
        ],
        SafetyCategory.SELF_HARM: [
            r"\b(suicidal|kill myself|self.?harm|cutting|end it all)\b",
            r"\b(cant go on|no point living|want to die)\b",
        ],
        SafetyCategory.SEXUAL: [
            r"\b(explicit|sexual|porn|nude|intercourse)\b",
            r"\b(ass|boob|breast|genital|penetration)\b",
        ],
        SafetyCategory.VIOLENCE: [
            r"\b(kill|murder|shoot|bomb|attack|stab|assault)\b",
            r"\b(destroy|torture|brutal|slaughter|massacre)\b",
        ],
    }
    return flags


def _find_unsafe_spans(
    text: str,
    flagged_categories: List[SafetyCategory],
) -> List[Dict]:
    """
    Find approximate unsafe spans in text based on flagged categories.
    Returns list of dicts with category, start, end, and matched_text.
    """
    flag_patterns = _build_category_regex_flags()
    spans = []

    for category in flagged_categories:
        if category not in flag_patterns:
            continue
        for pattern in flag_patterns[category]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                spans.append({
                    "category": category.value,
                    "start": match.start(),
                    "end": match.end(),
                    "matched_text": match.group(),
                })

    # Remove overlapping spans, keeping the longest
    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    filtered = []
    last_end = -1
    for span in spans:
        if span["start"] >= last_end:
            filtered.append(span)
            last_end = span["end"]

    return filtered


def redact_unsafe(
    text: str,
    redaction_char: str = "*",
    mode: str = "redact",
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Flag or redact unsafe spans from text using Azure AI Content Safety.

    Args:
        text: The user text to analyze and potentially redact.
        redaction_char: Character to use for redaction (default: '*').
        mode: Either 'redact' (replace spans) or 'flag' (mark with brackets).
        categories: Optional list of SafetyCategory to check.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        Dictionary with original text, processed text, flagged spans, and categories.
    """
    client = get_content_safety_client(endpoint=endpoint, api_key=api_key)

    request = SafetyRequest(text=text, categories=categories)
    azure_options = request.to_azure_options()

    try:
        raw_response = client.analyze_text(options=azure_options)
        result = parse_azure_response(raw_response)
    except HttpResponseError as e:
        return {
            "original_text": text,
            "processed_text": text,
            "flagged_spans": [],
            "categories": [],
            "error": str(e),
        }

    flagged_categories = result.flagged_categories
    spans = _find_unsafe_spans(text, flagged_categories)

    # Apply redaction or flagging
    processed = text
    if spans:
        if mode == "redact":
            # Apply in reverse order to preserve indices
            for span in sorted(spans, key=lambda s: s["start"], reverse=True):
                replacement = redaction_char * (span["end"] - span["start"])
                processed = processed[:span["start"]] + replacement + processed[span["end"]:]
        else:
            # Flag mode: wrap in brackets
            for span in sorted(spans, key=lambda s: s["start"], reverse=True):
                flagged = f"[UNSAFE:{span['category']}] {span['matched_text']} [/UNSAFE]"
                processed = processed[:span["start"]] + flagged + processed[span["end"]:]

    return {
        "original_text": text,
        "processed_text": processed,
        "flagged_spans": spans,
        "categories": [c.value for c in flagged_categories],
        "is_unsafe": result.is_unsafe,
    }


def redact_unsafe_json(
    text: str,
    redaction_char: str = "*",
    mode: str = "redact",
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Flag or redact unsafe spans and return JSON.

    Args:
        text: The user text to analyze.
        redaction_char: Character for redaction.
        mode: 'redact' or 'flag'.
        categories: Optional list of SafetyCategory.
        endpoint: Optional Azure endpoint override.
        api_key: Optional Azure API key override.

    Returns:
        JSON string of the redaction result.
    """
    import json
    result = redact_unsafe(
        text=text,
        redaction_char=redaction_char,
        mode=mode,
        categories=categories,
        endpoint=endpoint,
        api_key=api_key,
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "This is a hate message targeting a group."
    print(redact_unsafe_json(sample, mode="redact"))
