import os
from typing import Any, Dict

from openai import OpenAI

from safety_client import (
    get_openai_client,
    normalize_text_input,
    parse_moderation_response,
)


def moderate_text(text: Any) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    response = client.moderations.create(
        model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        input=normalize_text_input(text),
    )
    item = response.results[0]
    payload = {
        "flagged": bool(item.flagged),
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
        "decision": "block" if item.flagged else "allow",
    }
    return parse_moderation_response(payload).__dict__
