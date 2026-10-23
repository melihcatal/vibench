import os
from openai import OpenAI


def vendor_text_safety(vendor_notes: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=vendor_notes, model="text-moderation-3.5-turbo"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
        "safe_text": vendor_notes
        if not result.flagged
        else "[MODERATION_FLAGGED_CONTENT]",
    }
