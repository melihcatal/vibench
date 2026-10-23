from google.cloud import language_v1


def log_text_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload["text"]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    categories = [category.name for category in response.moderation_categories]
    return {"safe": not bool(categories), "categories": categories}
