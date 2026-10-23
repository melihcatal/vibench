
import os
from google.cloud import language_v1

def check_unsafe_content(text: str):
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    Args:
        text: The live transcript text to check.

    Returns:
        A dictionary containing the safety analysis results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform content moderation
    # The moderateText method is part of the Natural Language API's moderation features
    # and helps identify categories of potentially unsafe content.
    response = client.moderate_text(document=document)

    result = {}
    for category in response.moderation_categories:
        result[category.name] = category.score

    return result

