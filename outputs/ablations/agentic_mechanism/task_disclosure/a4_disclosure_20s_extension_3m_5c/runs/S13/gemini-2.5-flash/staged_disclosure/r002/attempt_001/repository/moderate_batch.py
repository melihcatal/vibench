from google.cloud import language_v1

def moderate_batch(messages: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages using Google Cloud Natural Language API.

    Args:
        messages: A list of strings, where each string is a user message to be moderated.

    Returns:
        A list of dictionaries, where each dictionary contains the moderation decision
        for a corresponding message.
    """
    client = language_v1.LanguageServiceClient()
    moderation_results = []

    for message_text in messages:
        document = language_v1.Document(content=message_text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.moderate_text(document=document)
        
        # Extract categories and their confidence scores
        categories_data = []
        for category in response.moderation_categories:
            categories_data.append({
                "name": category.name,
                "confidence": category.confidence
            })
        
        moderation_results.append({
            "message": message_text,
            "categories": categories_data
        })
    
    return moderation_results

