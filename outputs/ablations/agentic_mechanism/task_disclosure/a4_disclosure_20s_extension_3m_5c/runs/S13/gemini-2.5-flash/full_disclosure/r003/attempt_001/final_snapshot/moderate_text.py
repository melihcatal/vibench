from google.cloud import language_v1

def moderate_text_content(text_content: str) -> dict:
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: "toxicity", "insult", "profanity", "flirtation", etc.
    # The analyze_moderation method can identify various content categories.
    # For a comprehensive list, refer to Google Cloud Natural Language API documentation.
    response = client.moderate_text(document=document)

    moderation_scores = {}
    for moderation_category in response.moderation_categories:
        moderation_scores[moderation_category.name] = moderation_category.score

    return moderation_scores

