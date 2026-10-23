import openai


def claims_moderation(payload, config=None):
    client = openai.OpenAI(api_key=(config or {}).get("openai_api_key"))
    response = client.moderations.create(model="omni-moderation-latest", input=payload["text"])
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
