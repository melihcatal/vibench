from google.cloud import language_v1


def moderate_transcript(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    return {
        "status": "COMPLETED",
        "categories": [cat.name for cat in response.moderation_categories],
    }
