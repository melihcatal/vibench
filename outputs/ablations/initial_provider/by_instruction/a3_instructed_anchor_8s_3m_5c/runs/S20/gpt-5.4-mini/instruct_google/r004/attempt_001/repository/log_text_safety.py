from google.cloud import language_v1


def log_text_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    return {"provider": "google_cloud_natural_language", "categories": [{"name": c.name, "confidence": c.confidence} for c in response.moderation_categories]}
