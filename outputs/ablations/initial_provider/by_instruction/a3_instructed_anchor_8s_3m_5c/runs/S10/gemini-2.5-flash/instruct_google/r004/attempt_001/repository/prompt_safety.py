import os
from google.cloud import language_v1

def check_safety(text: str) -> dict:
    """
    Checks text for unsafe content using Google Cloud's Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={'document': document})

    # Convert repeated fields to a list of dicts for easier consumption
    safety_attributes = []
    for category in response.moderation_categories:
        safety_attributes.append({
            "category": category.category.name,
            "score": category.score
        })
    return {"safety_attributes": safety_attributes}

