import os
from openai import OpenAI
from document_models import SafetyResponse


def ocr_safety(text: str) -> SafetyResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    categories = {k: v for k, v in result.categories.items()}
    return {"flagged": result.flagged, "categories": categories}
