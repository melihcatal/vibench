import openai
import os


def check_payload_safety(payload: str) -> dict:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=payload)
    result = response.results[0]
    return {
        "is_safe": not result.flagged,
        "flagged_categories": result.categories,
        "category_scores": dict(result.category_scores),
    }
