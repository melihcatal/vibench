from openai import OpenAI


def live_caption_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.moderations.create(model="omni-moderation-latest", input=payload.get("text", ""))
    result = response.results[0]
    return {"unsafe": bool(result.flagged), "categories": result.categories.model_dump()}
