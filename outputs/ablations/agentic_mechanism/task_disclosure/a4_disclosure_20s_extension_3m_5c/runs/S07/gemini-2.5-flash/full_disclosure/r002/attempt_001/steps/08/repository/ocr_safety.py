from google.cloud import language_v1

def check_unsafe_content(text_content: str) -> dict:
    """
    Checks extracted document text for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text extracted from the document.

    Returns:
        A dictionary containing the moderation feedback.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: UNSPECIFIED, HARM_CATEGORY_TOXICITY, HARM_CATEGORY_SEXUALLY_EXPLICIT,
    # HARM_CATEGORY_DANGEROUS_CONTENT, HARM_CATEGORY_HATE_SPEECH, HARM_CATEGORY_HARASSMENT.
    # The analyze_moderation method can return scores for these categories.
    response = client.moderate_text(document=document)

    moderation_feedback = {}
    for moderation_category in response.moderation_categories:
        moderation_feedback[moderation_category.name.lower()] = moderation_category.score

    return moderation_feedback

