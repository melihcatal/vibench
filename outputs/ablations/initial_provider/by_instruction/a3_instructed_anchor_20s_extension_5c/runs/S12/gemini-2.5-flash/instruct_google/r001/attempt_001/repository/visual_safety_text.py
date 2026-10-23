from google.cloud import language_v1

def check_visual_labels_for_unsafe_text(text: str):
    """Checks generated visual labels for unsafe text using Google Cloud Natural Language API.

    This function performs sentiment and entity analysis to infer potential unsafety in text.
    For direct content moderation, consider using dedicated content moderation APIs if available.

    Args:
        text: The text string containing visual labels or descriptions to check.

    Returns:
        A dictionary indicating potential safety issues, e.g., {"sentiment_score": float, "sentiment_magnitude": float, "has_potentially_unsafe_keywords": bool}
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Perform entity analysis to look for potentially unsafe keywords (simplified for this example)
    # In a real-world scenario, a more robust keyword matching or a dedicated moderation API would be used.
    unsafe_keywords = ["kill", "hate", "violence", "porn", "sexual", "abuse", "weapon", "drug"]
    has_potentially_unsafe_keywords = any(keyword in text.lower() for keyword in unsafe_keywords)

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "has_potentially_unsafe_keywords": has_potentially_unsafe_keywords,
        "overall_safety_warning": (
            (sentiment.score < -0.5 and sentiment.magnitude > 1.0) or has_potentially_unsafe_keywords
        )
    }
