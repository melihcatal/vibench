from openai import OpenAI


def claims_moderation(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    text = payload.get("text", "")
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "provider": "openai"}
