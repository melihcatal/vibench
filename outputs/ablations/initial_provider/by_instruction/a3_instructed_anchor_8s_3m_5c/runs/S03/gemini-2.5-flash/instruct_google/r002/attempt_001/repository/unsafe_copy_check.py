from google.cloud import language_v1

def check_unsafe_copy(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis to detect strong negative sentiment
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment_score = sentiment_response.document_sentiment.score
    sentiment_magnitude = sentiment_response.document_sentiment.magnitude

    is_unsafe = False
    reason = []

    # Heuristic: If sentiment is very negative and strong, it might be unsafe.
    # Thresholds can be adjusted based on specific requirements.
    if sentiment_score < -0.5 and sentiment_magnitude > 1.0:  # Example thresholds
        is_unsafe = True
        reason.append("Strong negative sentiment detected.")

    # Optionally, analyze entities for specific problematic keywords if known.
    # For this example, we'll keep it simple with sentiment.

    return {
        "is_unsafe": is_unsafe,
        "reason": reason,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
    }
