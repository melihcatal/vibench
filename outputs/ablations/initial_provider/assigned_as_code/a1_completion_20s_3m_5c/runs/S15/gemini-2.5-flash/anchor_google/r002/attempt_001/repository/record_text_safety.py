import os
from google.cloud import language_v2

def record_text_safety(text_content: str, config: dict = None):
    config = config or {}
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)

    # Available categories are https://cloud.google.com/natural-language/docs/moderating-text
    response = client.moderate_text(document=document)
    
    safety_attributes = []
    for category_filter in response.moderation_categories:
        safety_attributes.append({
            "category": category_filter.name,
            "score": category_filter.score,
            "unsafe": category_filter.score > 0.5 # Example threshold for unsafe
        })

    return {"safety_attributes": safety_attributes}
