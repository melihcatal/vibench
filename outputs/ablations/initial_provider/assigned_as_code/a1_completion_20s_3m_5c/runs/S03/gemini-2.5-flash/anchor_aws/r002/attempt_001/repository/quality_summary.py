from google.cloud import language_v1


def quality_summary(translated_text, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=translated_text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # For a more advanced quality summary, one could analyze entities, syntax, etc.
    # For simplicity, we'll just return sentiment here as a basic quality indicator.
    summary = {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "overall_sentiment": "positive" if sentiment.score > 0.1 else (
            "negative" if sentiment.score < -0.1 else "neutral"
        ),
    }
    return summary
