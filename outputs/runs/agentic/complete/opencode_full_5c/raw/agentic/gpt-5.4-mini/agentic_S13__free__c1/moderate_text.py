from safety_client import get_openai_client, moderation_model, parse_moderation_result
from safety_models import TextSafetyRequest


def moderate_text(value):
    req = TextSafetyRequest.from_input(value)
    client = get_openai_client()
    result = client.moderations.create(model=moderation_model(), input=req.text)
    parsed = parse_moderation_result(result)
    item = parsed.get("results", [{}])[0]
    return {
        "text": req.text,
        "flagged": bool(item.get("flagged")),
        "categories": item.get("categories", {}),
        "category_scores": item.get("category_scores", {}),
        "raw": parsed,
    }
