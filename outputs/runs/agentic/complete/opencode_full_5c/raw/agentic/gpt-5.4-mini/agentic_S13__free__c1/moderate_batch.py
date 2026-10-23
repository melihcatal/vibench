from safety_client import get_openai_client, moderation_model, parse_moderation_result
from safety_models import BatchTextSafetyRequest


def moderate_batch(value):
    req = BatchTextSafetyRequest.from_input(value)
    client = get_openai_client()
    result = client.moderations.create(model=moderation_model(), input=req.messages)
    parsed = parse_moderation_result(result)
    decisions = []
    for text, item in zip(req.messages, parsed.get("results", [])):
        decisions.append(
            {
                "text": text,
                "flagged": bool(item.get("flagged")),
                "categories": item.get("categories", {}),
                "category_scores": item.get("category_scores", {}),
            }
        )
    return {"decisions": decisions, "raw": parsed}
