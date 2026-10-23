from google.cloud import language_v1

def moderate_transcript(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A simple moderation: flag if sentiment is very negative
    is_flagged = sentiment.score < -0.5 and sentiment.magnitude > 1.0

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_flagged_for_moderation": is_flagged,
        "moderation_reason": "Negative sentiment detected" if is_flagged else None,
    }
