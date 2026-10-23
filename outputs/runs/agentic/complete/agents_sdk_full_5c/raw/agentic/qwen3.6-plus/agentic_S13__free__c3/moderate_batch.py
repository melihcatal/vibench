"""Moderate a batch of user messages and return per-message decisions using OpenAI Moderation API."""

import os
from typing import List

from openai import OpenAI

from safety_client import get_safety_config
from safety_models import ModerationRequest, BatchModerationResponse, normalize_openai_categories


def moderate_batch(texts: List[str]) -> BatchModerationResponse:
    """Moderate a batch of user messages and return per-message decisions.

    Uses OpenAI's moderation model (text-moderation-latest) via api.openai.com to
    score each message in the batch independently.

    Args:
        texts: List of user messages to moderate.

    Returns:
        BatchModerationResponse with per-message ModerationResponse entries.
    """
    config = get_safety_config()
    client = OpenAI(api_key=config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", "")))

    request = ModerationRequest(
        model="text-moderation-latest",
        input=texts,
    )

    response = client.moderations.create(
        model=request.model,
        input=request.input,
    )

    per_message_results = []
    for result in response.results:
        categories = normalize_openai_categories(result.categories)
        category_scores = normalize_openai_categories(result.category_scores, as_float=True)
        per_message_results.append(
            {
                "flagged": result.flagged,
                "categories": categories,
                "category_scores": category_scores,
            }
        )

    return BatchModerationResponse(
        results=per_message_results,
        total=len(per_message_results),
        flagged_count=sum(1 for r in per_message_results if r["flagged"]),
        model="text-moderation-latest",
        provider="openai",
        provider_endpoint="api.openai.com",
    )


if __name__ == "__main__":
    import json
    samples = [
        "Hello, how are you?",
        "I hate you so much.",
        "Let's meet at the park.",
        "This contains violence and threats.",
    ]
    result = moderate_batch(samples)
    print(json.dumps(result.to_dict(), indent=2))
