from google.cloud import language_v1


def moderate_text_claim(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    categories = {}
    for category in response.moderation_categories:
        categories[category.name] = category.confidence

    return categories
