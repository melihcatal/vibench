import os
from openai import OpenAI


def moderate_vendor_text(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    moderation = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = moderation.results[0]

    categories = {}
    for cat in [
        "sexual",
        "hate",
        "harassment",
        "self-harm",
        "sexual/minors",
        "hate/threatening",
        "harassment/threatening",
        "violence",
        "violence/graphic",
    ]:
        try:
            categories[cat] = getattr(
                result.categories, cat.replace("/", "_").replace("-", "_"), False
            )
        except AttributeError:
            categories[cat] = False

    category_scores = {}
    for cat in [
        "sexual",
        "hate",
        "harassment",
        "self-harm",
        "sexual/minors",
        "hate/threatening",
        "harassment/threatening",
        "violence",
        "violence/graphic",
    ]:
        try:
            category_scores[cat] = getattr(
                result.category_scores, cat.replace("/", "_").replace("-", "_"), 0.0
            )
        except AttributeError:
            category_scores[cat] = 0.0

    return {
        "flagged": result.flagged,
        "categories": categories,
        "category_scores": category_scores,
        "model": "omni-moderation-latest",
        "provider": "openai",
        "input_text": text,
    }
