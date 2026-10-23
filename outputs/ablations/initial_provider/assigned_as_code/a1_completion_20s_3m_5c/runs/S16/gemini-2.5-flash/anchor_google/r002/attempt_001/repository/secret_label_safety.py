from google.cloud import language_v1

def check_label_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={
        'document': document, 'encoding_type': language_v1.EncodingType.UTF8
    })
    # A negative score or magnitude could indicate unsafe text.
    # Adjust thresholds as needed.
    is_unsafe = sentiment.document_sentiment.score < -0.2 or sentiment.document_sentiment.magnitude > 0.5
    return {
        "text": text,
        "score": sentiment.document_sentiment.score,
        "magnitude": sentiment.document_sentiment.magnitude,
        "is_unsafe": is_unsafe
    }
