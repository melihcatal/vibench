import openai


def profile_moderation(payload, config=None):
    config = config or {}
    openai.api_key = config.get("openai_api_key")
    response = openai.Moderation.create(model="omni-moderation-latest", input=payload["text"])
    result = response["results"][0]
    return {"flagged": result["flagged"], "categories": result["categories"]}
