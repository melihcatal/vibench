from google.cloud import language_v1

from speech_client import get_language_client

def moderate_transcript(payload: dict):
    client = get_language_client()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.moderate_text(request={"document": document})
    
    moderation_categories = []
    for category in response.moderation_categories:
        moderation_categories.append({
            "name": category.name,
            "confidence": category.confidence
        })
        
    return {"moderation_categories": moderation_categories}
