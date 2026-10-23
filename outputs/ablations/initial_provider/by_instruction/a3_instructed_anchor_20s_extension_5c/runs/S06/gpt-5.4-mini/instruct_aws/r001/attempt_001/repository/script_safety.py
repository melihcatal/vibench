import os

from openai import OpenAI


def check_script_safety(text, model=None):
    client = OpenAI()
    response = client.moderations.create(
        model=model or os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        input=text,
    )
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories), "scores": dict(result.category_scores)}
