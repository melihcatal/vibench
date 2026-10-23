import os
from openai import OpenAI

def moderate_claims(text: str) -> dict:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    response = client.moderations.create(input=text)
    moderation_output = response.results[0]
    
    return {
        "flagged": moderation_output.flagged,
        "categories": moderation_output.categories.model_dump(),
        "category_scores": moderation_output.category_scores.model_dump(),
    }
