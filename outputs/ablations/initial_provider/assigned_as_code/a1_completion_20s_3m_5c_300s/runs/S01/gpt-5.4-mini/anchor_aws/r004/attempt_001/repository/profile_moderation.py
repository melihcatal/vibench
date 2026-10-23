from openai import OpenAI


def profile_moderation(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    moderation = client.moderations.create(
        model=(config or {}).get("model", "omni-moderation-latest"),
        input=payload["text"],
    )
    result = moderation.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
