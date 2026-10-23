
from google.cloud import language_v1

def moderate_text(text_content: str):
    """
    Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.
    This function uses text classification to identify categories that might indicate unsafe content.
    For more explicit content moderation, a dedicated moderation API would be preferred if available.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify the text into categories. These categories can then be evaluated
    # for potential unsafe or policy-violating content based on application logic.
    response = client.classify_text(request={"document": document})

    # You can process the categories here to determine if the content is unsafe.
    # For example, look for categories like "/Adult", "/Sensitive Subjects", etc.
    # The interpretation of 'unsafe' depends on the application's policy.
    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    return {"text": text_content, "categories": categories}

