from google.cloud import language_v1

def live_caption_safety(caption_text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=caption_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    # For simplicity, we'll just return sentiment score as a proxy for safety check.
    # In a real scenario, more sophisticated analysis with custom models or other APIs would be used.
    return {
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "is_safe": response.document_sentiment.score >= -0.2 # Arbitrary threshold for demonstration
    }
