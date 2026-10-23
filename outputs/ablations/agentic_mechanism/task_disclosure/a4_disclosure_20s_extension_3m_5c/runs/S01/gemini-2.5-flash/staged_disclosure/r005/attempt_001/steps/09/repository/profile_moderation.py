from google.cloud import language_v1

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud Natural Language API.

    Args:
        text: The profile text to moderate.

    Returns:
        A dictionary containing moderation results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects sentiment (optional, but a common moderation step)
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Classifies content to identify potentially problematic categories
    # Note: Content classification might not directly provide "profanity" or "toxicity" scores
    # but can categorize content into areas like "Social Media", "Violent Content", etc.
    # For explicit profanity/toxicity, other specialized APIs or custom models might be needed.
    # For simplicity, we'll use classify_text here and interpret its output for moderation.
    # A more robust solution might involve custom entity recognition or sentiment analysis for specific keywords.
    classify_response = client.classify_text(document=document)
    categories = classify_response.categories

    # For demonstration, we'll create a simple moderation decision based on sentiment and categories.
    # In a real-world scenario, you'd have more sophisticated rules and potentially
    # integrate with a dedicated content moderation API that provides explicit scores for
    # profanity, toxicity, etc.

    needs_moderation = False
    moderation_flags = []

    if sentiment.score < -0.2:  # Example threshold for negative sentiment
        needs_moderation = True
        moderation_flags.append("negative_sentiment")

    for category in categories:
        # Example: if content is categorized as "Violent Content", flag it.
        # This is a simplification; actual categories and thresholds would depend on requirements.
        if "Violent Content" in category.name or "Hate Speech" in category.name:
            needs_moderation = True
            moderation_flags.append(f"categorized_as_{category.name.replace('/', '_').lower()}")

    return {
        "text": text,
        "needs_moderation": needs_moderation,
        "moderation_flags": moderation_flags,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "categories": [{"name": c.name, "confidence": c.confidence} for c in categories]
    }

if __name__ == "__main__":
    # Example usage:
    profile_text_1 = "I love this new platform! It's amazing."
    result_1 = moderate_profile_text(profile_text_1)
    print(f"Profile Text 1: \'{profile_text_1}\'")
    print(f"Moderation Result 1: {result_1}\n")

    profile_text_2 = "This platform is terrible. I hate it. You all suck."
    result_2 = moderate_profile_text(profile_text_2)
    print(f"Profile Text 2: \'{profile_text_2}\'")
    print(f"Moderation Result 2: {result_2}\n")

    profile_text_3 = "Just sharing some thoughts on current events."
    result_3 = moderate_profile_text(profile_text_3)
    print(f"Profile Text 3: \'{profile_text_3}\'")
    print(f"Moderation Result 3: {result_3}\n")
