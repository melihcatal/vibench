from openai import OpenAI


def live_caption_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.moderations.create(model=config.get("model", "omni-moderation-latest"), input=payload["text"])
    result = response.results[0]
    return {"text": payload["text"], "is_flagged": bool(result.flagged), "categories": dict(result.categories)}
