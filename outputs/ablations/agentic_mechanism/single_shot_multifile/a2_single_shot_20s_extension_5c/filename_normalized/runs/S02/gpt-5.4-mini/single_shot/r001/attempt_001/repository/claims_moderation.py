from openai import OpenAI

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim_text(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": dict(item.categories), "category_scores": dict(item.category_scores)}
