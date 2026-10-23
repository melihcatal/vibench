from google.cloud import language_v2

def check_unsafe_text(text: str) -> bool:
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    for category_score in response.document_metadata.get("moderation_categories", []):
        if category_score.score > 0.5:
            return False
    return True
