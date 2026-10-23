from google.cloud import language_v1

def summarize_translation_quality_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of translated text as a basic quality check
    using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "description": "Sentiment score ranges from -1 (negative) to 1 (positive) and magnitude indicates the overall strength of emotion."
    }
