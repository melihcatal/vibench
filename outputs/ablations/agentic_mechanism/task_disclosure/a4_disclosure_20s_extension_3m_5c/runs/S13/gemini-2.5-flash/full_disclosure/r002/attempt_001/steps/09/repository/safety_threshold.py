from google.cloud import language_v1

def apply_thresholds(text_content: str, thresholds: dict) -> dict:
    """
    Applies category thresholds to decide whether to allow text.

    Args:
        text_content: The user text to be moderated.
        thresholds: A dictionary where keys are moderation categories (e.g., 'TOXICITY')
                    and values are the corresponding float thresholds (0.0 to 1.0).

    Returns:
        A dictionary with the decision and details:
        {'allowed': True/False, 'reasons': ['category_exceeded_threshold', ...]}
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Use the Google Cloud Natural Language API for text moderation
    # The provider is identified by 'google.cloud.language_v1' and 'language_v1.LanguageServiceClient'
    response = client.moderate_text(document=document)

    allowed = True
    reasons = []
    
    # Placeholder for moderation categories from the API.
    # In a real scenario, you would map API categories to your threshold categories.
    # For demonstration, let's assume 'TOXICITY', 'SEXUAL', 'VIOLENCE' are possible categories
    # and map them to their scores.
    
    # Google Cloud Natural Language API's moderate_text returns a list of categories
    # with a score. We iterate through these to apply our custom thresholds.
    
    # Note: The actual categories returned by Google Cloud's moderate_text API might differ.
    # This is a conceptual mapping. For example:
    # 'HARM_CATEGORY_TOXICITY', 'HARM_CATEGORY_SEXUAL', 'HARM_CATEGORY_VIOLENCE', etc.
    # For this example, we assume `response.moderation_categories` exists and has a similar structure
    # to what's described in the API documentation or common content moderation responses.
    
    # A simplified example of processing moderation scores from a generic API response
    # In a real implementation, you would need to inspect the exact structure of `response`
    # from the Google Cloud Language API's `moderate_text` method.
    
    # As per Google Cloud Natural Language API, the moderate_text response contains `moderation_categories`
    # each with a name and a score.
    
    if hasattr(response, 'moderation_categories'):
        for category_score in response.moderation_categories:
            category_name = category_score.name.upper() # e.g., "TOXICITY"
            score = category_score.score # e.g., 0.9
            
            if category_name in thresholds:
                if score > thresholds[category_name]:
                    allowed = False
                    reasons.append(f"{category_name}_exceeded_threshold")

    return {'allowed': allowed, 'reasons': reasons}
