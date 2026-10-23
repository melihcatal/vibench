from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os

def ocr_safety(text: str, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeContent
    response = client.classify_text(document=document)

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    return {"safety_attributes": categories}
