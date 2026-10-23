from openai import OpenAI

from speech_models import ModerationRequest


def moderate_transcript(text):
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {
        "flagged": item.flagged,
        "categories": item.categories.model_dump(),
        "category_scores": item.category_scores.model_dump(),
    }
