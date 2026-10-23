from google.cloud import language_v1

def check_unsafe_content(text_content: str):
    """
    Checks the input text for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text extracted from a document.

    Returns:
        A dictionary containing safety attributes and their scores.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/reference/rest/v1/projects.documents/annotateText#categories
    response = client.classify_text(request={"document": document})

    safety_attributes = {}
    for category in response.categories:
        safety_attributes[category.name] = category.confidence

    return safety_attributes

