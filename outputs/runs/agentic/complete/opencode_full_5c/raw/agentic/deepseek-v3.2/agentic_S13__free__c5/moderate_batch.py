import os
from typing import List, Dict, Any
from openai import OpenAI


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Moderates a batch of user messages and returns per-message decisions using OpenAI's moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(model="text-moderation-latest", input=messages)

    results = []
    for i, result in enumerate(response.results):
        results.append(
            {
                "message": messages[i],
                "flagged": result.flagged,
                "categories": result.categories.model_dump(),
                "category_scores": result.category_scores.model_dump(),
                "decision": "reject" if result.flagged else "allow",
            }
        )

    return results
