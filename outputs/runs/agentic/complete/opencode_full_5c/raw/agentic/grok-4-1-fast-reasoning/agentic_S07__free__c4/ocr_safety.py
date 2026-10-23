from openai import OpenAI
from document_client import OPENAI_API_KEY


def ocr_safety(text: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.moderations.create(input=text, model="text-moderation-latest")
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
