from openai import OpenAI

from speech_models import normalize_text


def check_script_safety(text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=normalize_text(text),
    )
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories)}
