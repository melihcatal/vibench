"""
[SAME-SCENARIO] moderate_text.py
Scores user text for unsafe or policy-violating content using the OpenAI Moderation API.
Provider: OpenAI — model identifier: text-moderation-latest
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any

from safety_client import get_openai_client, load_safety_config
from safety_models import (
    ModerationResult,
    CategoryScore,
    ModerationDecision,
    normalize_openai_moderation_response,
)

DEFAULT_MODEL = "text-moderation-latest"


def moderate_text(
    text: str,
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> ModerationResult:
    """
    Score a single text string for unsafe or policy-violating content
    using the OpenAI Moderation API (model: text-moderation-latest).
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)
    response = client.moderations.create(
        input=text,
        model=model,
    )

    result = normalize_openai_moderation_response(text, response)
    result.metadata["provider"] = "openai"
    result.metadata["model"] = model
    result.metadata["api_endpoint"] = "api.openai.com"

    return result


def moderate_text_with_decision(
    text: str,
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Score text and return a decision-oriented response dict
    suitable for API consumers.
    """
    result = moderate_text(text, model=model, config=config)
    return result.to_dict()


if __name__ == "__main__":
    sample = "This is a normal, safe message."
    decision = moderate_text_with_decision(sample)
    print(decision)
