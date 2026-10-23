from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client, moderation_model_name
from safety_models import normalize_threshold_result


def apply_threshold(text: str, thresholds: Dict[str, float] | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    model = moderation_model_name()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Score the text for moderation categories and determine allow/deny using the provided thresholds. Return JSON with category_scores, threshold_decision, and explanation.",
            },
            {
                "role": "user",
                "content": text if thresholds is None else f"THRESHOLDS: {thresholds}\nTEXT: {text}",
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    return normalize_threshold_result(response.output_text, thresholds)
