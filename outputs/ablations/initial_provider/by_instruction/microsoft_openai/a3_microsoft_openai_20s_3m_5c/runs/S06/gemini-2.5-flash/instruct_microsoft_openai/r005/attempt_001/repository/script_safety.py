import os
from openai import OpenAI

def check_script_safety(text: str) -> dict:
    """
    Checks narration scripts for unsafe content using OpenAI's Moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)

    moderation_result = response.results[0]
    return {
        "flagged": moderation_result.flagged,
        "categories": moderation_result.categories.model_dump(),
        "category_scores": moderation_result.category_scores.model_dump()
    }
