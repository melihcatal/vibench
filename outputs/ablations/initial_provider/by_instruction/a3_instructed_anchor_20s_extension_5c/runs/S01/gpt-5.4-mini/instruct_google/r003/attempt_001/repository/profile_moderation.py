from openai import OpenAI


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
