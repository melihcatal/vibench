import openai


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = openai.OpenAI(api_key=config.get("api_key"))
    response = client.moderations.create(model=config.get("moderation_model", "omni-moderation-latest"), input=payload.get("text", ""))
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories, "category_scores": result.category_scores}
