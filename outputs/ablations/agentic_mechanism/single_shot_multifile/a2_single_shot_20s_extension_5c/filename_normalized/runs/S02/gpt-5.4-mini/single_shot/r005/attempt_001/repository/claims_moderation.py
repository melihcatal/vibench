from openai import OpenAI


def moderate_claims_text(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": dict(item.categories), "category_scores": dict(item.category_scores)}
