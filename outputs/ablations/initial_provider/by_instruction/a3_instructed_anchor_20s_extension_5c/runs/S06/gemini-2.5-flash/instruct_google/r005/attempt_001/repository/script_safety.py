from google.cloud import language_v1

def check_safety(text: str) -> dict:
    """Checks narration scripts for unsafe content using Google Cloud Natural Language API.

    Returns a dictionary of categories and their confidence scores.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify the document content
    response = client.classify_text(request={'document': document})

    safety_analysis = {}
    for category in response.categories:
        # The API returns categories like /Adult/Violent, /Science/Technology/Computers, etc.
        # We can define what constitutes "unsafe" based on the task requirements.
        # For this example, we'll just return all categories and their confidence.
        safety_analysis[category.name] = category.confidence

    return safety_analysis
