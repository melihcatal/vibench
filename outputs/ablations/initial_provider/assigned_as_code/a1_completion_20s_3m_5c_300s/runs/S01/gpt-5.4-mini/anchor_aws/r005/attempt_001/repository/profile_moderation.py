from openai import OpenAI


def profile_moderation(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.moderations.create(model="omni-moderation-latest", input=payload["text"])
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump()}
