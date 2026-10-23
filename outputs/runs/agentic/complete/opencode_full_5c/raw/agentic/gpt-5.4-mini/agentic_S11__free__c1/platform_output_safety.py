from openai import OpenAI

from model_models import normalize_text


def platform_output_safety(text: str) -> dict:
    client = OpenAI()
    moderation = client.moderations.create(
        model="omni-moderation-latest", input=normalize_text(text)
    )
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "model": "omni-moderation-latest",
    }
