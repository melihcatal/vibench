import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from messaging_models import normalize_payload, extract_text_from_payload


def check_message_safety(
    message_data: Dict[str, Any], categories: Optional[list] = None
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    payload = normalize_payload(message_data.get("data", message_data))
    text = extract_text_from_payload(payload)

    if not text or len(text.strip()) == 0:
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "message_id": message_data.get("message_id", "unknown"),
            "provider": "openai-moderation",
            "model": "omni-moderation-latest",
            "status": "no_content",
        }

    moderation = client.moderations.create(input=text, model="omni-moderation-latest")

    result = moderation.results[0]
    flagged = result.flagged

    category_flags = {}
    category_scores = {}

    for cat_name, is_flagged in result.categories.model_dump().items():
        category_flags[cat_name] = is_flagged

    for cat_name, score in result.category_scores.model_dump().items():
        category_scores[cat_name] = round(score, 4)

    if categories:
        category_flags = {k: v for k, v in category_flags.items() if k in categories}
        category_scores = {k: v for k, v in category_scores.items() if k in categories}

    return {
        "flagged": flagged,
        "categories": category_flags,
        "category_scores": category_scores,
        "message_id": message_data.get("message_id", "unknown"),
        "provider": "openai-moderation",
        "model": "omni-moderation-latest",
        "status": "safe" if not flagged else "unsafe",
    }


def batch_check_safety(messages: list[Dict[str, Any]]) -> Dict[str, Any]:
    results = []
    overall_flagged = False

    for msg in messages:
        safety_result = check_message_safety(msg)
        results.append(safety_result)
        if safety_result["flagged"]:
            overall_flagged = True

    return {
        "results": results,
        "total_checked": len(messages),
        "total_flagged": sum(1 for r in results if r["flagged"]),
        "overall_safe": not overall_flagged,
        "provider": "openai-moderation",
        "model": "omni-moderation-latest",
    }


if __name__ == "__main__":
    sample_message = {
        "message_id": "msg_safety_001",
        "data": {"text": "Hello, this is a friendly message from a customer."},
    }
    result = check_message_safety(sample_message)
    print(json.dumps(result, indent=2))
