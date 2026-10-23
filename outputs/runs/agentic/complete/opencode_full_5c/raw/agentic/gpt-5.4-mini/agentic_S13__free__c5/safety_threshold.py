import os
from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client, get_threshold_env, normalize_text_input


def safety_threshold(text: Any) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    response = client.moderations.create(
        model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        input=normalize_text_input(text),
    )
    result = response.results[0]
    thresholds = {
        "harassment": get_threshold_env("SAFETY_THRESHOLD_HARASSMENT", 0.5),
        "hate": get_threshold_env("SAFETY_THRESHOLD_HATE", 0.5),
        "self-harm": get_threshold_env("SAFETY_THRESHOLD_SELF_HARM", 0.3),
        "sexual": get_threshold_env("SAFETY_THRESHOLD_SEXUAL", 0.5),
        "violence": get_threshold_env("SAFETY_THRESHOLD_VIOLENCE", 0.5),
    }
    scores = dict(result.category_scores)
    allowed = True
    for category, threshold in thresholds.items():
        if float(scores.get(category, 0.0)) >= threshold:
            allowed = False
    return {
        "allowed": allowed,
        "flagged": bool(result.flagged),
        "scores": scores,
        "thresholds": thresholds,
    }
