from typing import Any, Dict, Iterable, List
from safety_client import get_openai_client, get_moderation_model_name
from safety_models import normalize_batch_texts, build_batch_moderation_result


def moderate_batch(messages: Iterable[str], *, model: str | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    items = normalize_batch_texts(messages)
    model_name = model or get_moderation_model_name()
    response = client.moderations.create(model=model_name, input=[item["text"] for item in items])
    decisions: List[Dict[str, Any]] = []
    for item, result in zip(items, response.results):
        decisions.append(
            {
                "index": item["index"],
                "text": item["text"],
                "flagged": bool(result.flagged),
                "categories": dict(result.categories),
                "category_scores": dict(result.category_scores),
            }
        )
    return build_batch_moderation_result(decisions=decisions, model=model_name)


if __name__ == "__main__":
    raise SystemExit(0)
