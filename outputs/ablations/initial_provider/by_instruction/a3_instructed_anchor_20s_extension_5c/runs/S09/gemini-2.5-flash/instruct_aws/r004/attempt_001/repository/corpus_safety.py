from google.cloud import language_v2

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of a given text using Google Cloud's Natural Language API.

    Args:
        text: The text string to check for safety.

    Returns:
        A dictionary containing safety attributes and their scores.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)

    # Perform moderate_text to check for safety attributes
    response = client.moderate_text(document=document)

    safety_attributes = {}
    for category in response.moderation_categories:
        safety_attributes[category.name] = category.score

    return safety_attributes
