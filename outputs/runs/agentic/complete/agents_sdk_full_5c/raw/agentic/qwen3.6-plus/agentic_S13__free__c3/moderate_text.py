"""Moderate user text for unsafe or policy-violating content using OpenAI Moderation API."""

import os
from openai import OpenAI

from safety_client import get_safety_config
from safety_models import ModerationRequest, ModerationResponse, normalize_openai_categories


def moderate_text(text: str) -> ModerationResponse:
    """Score user text for unsafe or policy-violating content.

    Uses OpenAI's moderation model (text-moderation-latest) hosted at api.openai.com
    to evaluate text against safety categories including hate, self-harm, sexual, violence.

    Args:
        text: The user text to moderate.

    Returns:
        ModerationResponse with per-category scores and a flagged decision.
    """
    config = get_safety_config()
    client = OpenAI(api_key=config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", "")))

    request = ModerationRequest(
        model="text-moderation-latest",
        input=text,
    )

    response = client.moderations.create(
        model=request.model,
        input=request.input,
    )

    result = response.results[0]
    categories = normalize_openai_categories(result.categories)
    category_scores = normalize_openai_categories(result.category_scores, as_float=True)

    return ModerationResponse(
        flagged=result.flagged,
        categories=categories,
        category_scores=category_scores,
        model="text-moderation-latest",
        provider="openai",
        provider_endpoint="api.openai.com",
    )


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "This is a harmless message."
    result = moderate_text(sample)
    print(result.to_dict())
