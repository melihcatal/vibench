import os
from openai import OpenAI

def moderate_profile_text(text: str) -> dict:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = OpenAI(api_key=openai_api_key)

    # Using OpenAI's moderation API for content filtering
    # OpenAI API hostname: api.openai.com
    response = client.moderations.create(input=text)

    moderation_result = response.results[0]
    return {
        "flagged": moderation_result.flagged,
        "categories": moderation_result.categories.model_dump(),
        "category_scores": moderation_result.category_scores.model_dump()
    }
