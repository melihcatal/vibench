import os
from openai import OpenAI

def check_script_safety(text: str) -> dict:
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    response = client.moderations.create(input=text, model="text-moderation-latest")

    moderation_result = response.results[0]

    return {
        "flagged": moderation_result.flagged,
        "categories": {
            category.name: category.violated for category in moderation_result.categories
        },
        "category_scores": {
            category.name: category.score for category in moderation_result.category_scores
        }
    }
