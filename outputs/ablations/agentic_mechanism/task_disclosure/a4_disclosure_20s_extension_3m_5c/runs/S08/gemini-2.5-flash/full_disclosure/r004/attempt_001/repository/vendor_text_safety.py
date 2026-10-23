from google.cloud import language_v1

def moderate_vendor_text(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using Google Cloud Natural Language API.

    Args:
        text: The text content to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.moderate_text(document=document)
    
    # Convert repeated composite fields to a list of dictionaries for easier handling if needed
    moderation_categories = []
    for category in response.moderation_categories:
        moderation_categories.append({
            "name": category.name,
            "score": category.score
        })

    return {"moderation_categories": moderation_categories}

