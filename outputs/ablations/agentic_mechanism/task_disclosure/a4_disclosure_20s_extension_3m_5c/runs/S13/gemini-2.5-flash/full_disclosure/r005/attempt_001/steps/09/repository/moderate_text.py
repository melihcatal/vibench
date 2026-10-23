import os
from google.cloud import language_v2

def moderate_text_content(text_content: str):
    """
    Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.

    Args:
        text_content: The user text to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )
    
    # Perform moderation
    response = client.moderate_text(document=document)

    # Convert the response to a dictionary for easier handling/return
    # This is a basic conversion; actual use might require more sophisticated parsing
    moderation_results = []
    for category_score in response.moderation_categories:
        moderation_results.append({
            "category": category_score.category.name,
            "score": category_score.score
        })
    
    return {"moderation_categories": moderation_results}

