from google.cloud import language_v1 as language


def moderate_transcript(payload, config=None):
    config = config or {}
    client = language.LanguageServiceClient()
    document = language.Document(content=payload["text"], type_=language.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    categories = []
    for moderation in response.moderation_categories:
        categories.append({"name": moderation.name, "confidence": moderation.confidence})
    return {"status": "COMPLETED", "categories": categories}
