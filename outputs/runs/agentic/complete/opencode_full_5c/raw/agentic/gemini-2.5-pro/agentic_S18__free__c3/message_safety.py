from google.cloud import language_v1


def check_message_safety(text: str) -> dict:
    """
    Checks message payload text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    safety_categories = {
        category.name: category.confidence
        for category in response.moderation_categories
    }

    is_safe = all(confidence < 0.5 for confidence in safety_categories.values())

    return {"is_safe": is_safe, "categories": safety_categories}
