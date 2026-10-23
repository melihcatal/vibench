from google.cloud import language_v1


def ocr_safety(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={'document': document})
    return {'moderation_categories': [c.name for c in response.moderation_categories], 'moderation_scores': [c.confidence for c in response.moderation_categories]}
