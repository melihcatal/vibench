import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI

from safety_client import (
    get_openai_client,
    normalize_batch_input,
    parse_batch_moderation_response,
)


def moderate_batch(messages: Iterable[Any]) -> List[Dict[str, Any]]:
    client: OpenAI = get_openai_client()
    normalized = normalize_batch_input(messages)
    response = client.moderations.create(
        model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        input=normalized,
    )
    items = []
    for result in response.results:
        items.append(
            {
                "flagged": bool(result.flagged),
                "categories": dict(result.categories),
                "category_scores": dict(result.category_scores),
                "decision": "block" if result.flagged else "allow",
            }
        )
    return [r.__dict__ for r in parse_batch_moderation_response(items).results]
