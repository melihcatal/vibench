
from google.cloud import language_v1

def check_unsafe_content(text: str) -> dict:
    """
    Checks the extracted document text for unsafe content using Google Cloud Natural Language API.

    Args:
        text: The document text to check.

    Returns:
        A dictionary containing the safety moderation results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-text#categories_of_content
    response = client.moderate_text(document=document)

    result = {}
    for category_filter in response.moderation_categories:
        result[category_filter.name] = category_filter.score

    return result

