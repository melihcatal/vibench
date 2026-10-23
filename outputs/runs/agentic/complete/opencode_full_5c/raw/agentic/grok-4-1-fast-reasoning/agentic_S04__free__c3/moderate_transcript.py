import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def moderate_transcript(text: str) -> dict:
    response = openai.moderation.create(input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
