from google.cloud import language_v1

def check_live_caption_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment
    
    response = client.moderate_text(
        request={"document": document}
    )
    moderation = response.moderation_categories
    
    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "toxicity": next(
            (cat.confidence for cat in moderation if cat.name == "Toxicity"), 0.0
        ),
        "identity_attack": next(
            (cat.confidence for cat in moderation if cat.name == "Identity attack"), 0.0
        ),
        "profanity": next(
            (cat.confidence for cat in moderation if cat.name == "Profanity"), 0.0
        ),
    }