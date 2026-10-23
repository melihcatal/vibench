"""Check message payload text for unsafe content using OpenAI Moderation API.

Uses the openai SDK moderation endpoint to analyze message payloads for
potentially harmful, inappropriate, or unsafe content before processing.
"""

import os
import json
from typing import Optional, Dict, Any, List

from openai import OpenAI


def check_message_safety(
    text: str,
    categories_threshold: Optional[Dict[str, float]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Check message text for unsafe content using OpenAI moderation.

    Args:
        text: Text content to analyze for safety.
        categories_threshold: Optional custom thresholds per category.
            Defaults are used if not provided.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Dict with safety analysis results including flagged categories.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(input=text)
    result = response.results[0]

    categories = {}
    category_scores = {}

    for category_name, flagged in result.categories.model_dump().items():
        if flagged is not None:
            categories[category_name] = flagged

    for category_name, score in result.category_scores.model_dump().items():
        if score is not None:
            category_scores[category_name] = round(score, 4)

    default_thresholds = {
        "hate": 0.5,
        "hate/threatening": 0.3,
        "self-harm": 0.3,
        "sexual": 0.5,
        "sexual/minors": 0.1,
        "violence": 0.5,
        "violence/graphic": 0.3,
    }
    thresholds = categories_threshold or default_thresholds

    flagged_categories = []
    for cat_name, is_flagged in categories.items():
        if is_flagged:
            flagged_categories.append(cat_name)
        elif cat_name in category_scores:
            score = category_scores[cat_name]
            threshold = thresholds.get(cat_name, 0.5)
            if score >= threshold:
                flagged_categories.append(cat_name)

    is_safe = result.flagged and len(flagged_categories) == 0 or not result.flagged

    return {
        "status": "analyzed",
        "is_safe": is_safe and not flagged_categories,
        "flagged": bool(flagged_categories),
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "overall_flagged": result.flagged,
    }


def check_batch_safety(
    messages: List[Dict[str, Any]],
    text_field: str = "text",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Check multiple messages for unsafe content.

    Args:
        messages: List of message dicts containing text to analyze.
        text_field: Key in each dict containing the text to check.
        api_key: OpenAI API key.

    Returns:
        Dict with batch safety analysis results.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    texts = []
    message_ids = []
    for msg in messages:
        text = msg.get(text_field, msg.get("payload", {}).get("text", ""))
        if text:
            texts.append(text)
            message_ids.append(msg.get("event_id", msg.get("message_id", "unknown")))

    if not texts:
        return {
            "status": "no_text_to_analyze",
            "results": [],
        }

    # OpenAI moderation supports batch input
    response = client.moderations.create(input=texts)

    results = []
    unsafe_count = 0

    for i, mod_result in enumerate(response.results):
        flagged_cats = [
            cat for cat, val in mod_result.categories.model_dump().items()
            if val is not None and val
        ]
        is_unsafe = mod_result.flagged or len(flagged_cats) > 0
        if is_unsafe:
            unsafe_count += 1

        results.append({
            "message_id": message_ids[i] if i < len(message_ids) else f"index-{i}",
            "is_safe": not is_unsafe,
            "flagged_categories": flagged_cats,
            "overall_flagged": mod_result.flagged,
        })

    return {
        "status": "batch_analyzed",
        "total_checked": len(results),
        "unsafe_count": unsafe_count,
        "safe_count": len(results) - unsafe_count,
        "results": results,
    }


def extract_and_check_payload(
    message_data: Dict[str, Any],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract text from a message payload and check for safety.

    Automatically finds text content in common payload fields.

    Args:
        message_data: Message dict with payload.
        api_key: OpenAI API key.

    Returns:
        Dict with safety analysis and extracted text.
    """
    payload = message_data.get("payload", message_data)
    text = ""

    for key in ["text", "content", "message", "body", "description", "comment"]:
        if key in payload and isinstance(payload[key], str):
            text = payload[key]
            break

    if not text:
        text = json.dumps(payload)

    safety_result = check_message_safety(text, api_key=api_key)
    safety_result["extracted_text_preview"] = text[:200]

    return safety_result


if __name__ == "__main__":
    sample_text = "This is a normal customer message about order #12345."
    result = check_message_safety(sample_text)
    print(json.dumps(result, indent=2))
