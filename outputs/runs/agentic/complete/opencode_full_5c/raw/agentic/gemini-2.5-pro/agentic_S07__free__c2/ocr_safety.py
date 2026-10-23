from google.cloud import language_v1


def check_text_safety(text: str):
    """
    Checks text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    safety_categories = {}
    for category in response.moderation_categories:
        safety_categories[category.name] = category.confidence

    return safety_categories
