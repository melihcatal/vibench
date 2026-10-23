import os
from openai import OpenAI


def vendor_text_safety(vendor_text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set")
    response = client.moderations.create(
        input=vendor_text, model="text-moderation-3.5-ada"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
