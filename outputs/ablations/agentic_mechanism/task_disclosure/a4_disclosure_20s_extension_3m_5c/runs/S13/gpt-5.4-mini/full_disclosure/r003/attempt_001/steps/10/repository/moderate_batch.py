import json
import os
import sys
from typing import Any, Dict, Iterable, List, Optional, Sequence

from openai import OpenAI


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if isinstance(value, dict):
        return dict(value)
    return dict(value)


def moderate_batch(messages: Sequence[str], model: Optional[str] = None) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation_model = model or os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    response = client.moderations.create(model=moderation_model, input=list(messages))
    decisions: List[Dict[str, Any]] = []
    for index, result in enumerate(response.results):
        categories = _to_dict(result.categories)
        category_scores = _to_dict(result.category_scores)
        decisions.append(
            {
                "index": index,
                "model": moderation_model,
                "flagged": bool(result.flagged),
                "categories": categories,
                "category_scores": category_scores,
            }
        )
    return decisions


def main() -> None:
    payload = sys.stdin.read().strip()
    messages = json.loads(payload) if payload else []
    output = moderate_batch(messages)
    sys.stdout.write(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
