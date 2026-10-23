import openai
import os
from document_models import SafetyResult


def ocr_safety(text: str) -> SafetyResult:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories_scores": result.categories_scores}
