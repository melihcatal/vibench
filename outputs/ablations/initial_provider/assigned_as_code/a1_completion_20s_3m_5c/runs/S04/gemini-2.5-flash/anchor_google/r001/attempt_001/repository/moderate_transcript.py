from google.cloud import language_v1

def moderate_transcript(text_content: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A simple moderation check based on sentiment score
    moderation_status = "CLEAN"
    if sentiment.score < -0.5:
        moderation_status = "NEEDS_REVIEW_NEGATIVE"
    elif sentiment.score > 0.5:
        moderation_status = "POSITIVE"

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "moderation_status": moderation_status,
    }
