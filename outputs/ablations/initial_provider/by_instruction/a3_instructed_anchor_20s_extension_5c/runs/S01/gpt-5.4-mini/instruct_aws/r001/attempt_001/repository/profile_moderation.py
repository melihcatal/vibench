import openai

from identity_models import TextRequest, to_payload


def profile_moderation(text: str):
    payload = to_payload(TextRequest(text=text))
    client = openai.OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=payload["text"])
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
