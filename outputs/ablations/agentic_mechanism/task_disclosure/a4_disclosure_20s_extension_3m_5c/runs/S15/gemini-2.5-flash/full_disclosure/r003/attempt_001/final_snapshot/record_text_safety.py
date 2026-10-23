from google.cloud import language_v1

def check_unsafe_content(text_content: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a general idea of the content's safety.
    # For more robust content moderation, other APIs like Google Cloud Video Intelligence API
    # or custom solutions might be more suitable. This is a basic example using Natural Language API.
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # You can define your own thresholds for what constitutes "unsafe" based on sentiment scores.
    # For demonstration, we'll consider highly negative sentiment as potentially unsafe.
    is_unsafe = sentiment.score < -0.5

    return {
        "text_content": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_potentially_unsafe": is_unsafe
    }
