from google.cloud import language_v1

def metric_annotation_safety(payload: dict, config: dict = None) -> dict:
    config = config or {}

    client = language_v1.LanguageServiceClient()
    
    text_content = payload.get("annotation_text")
    if not text_content:
        raise ValueError("annotation_text must be provided in payload")

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment to get a general idea, can be extended for explicit content detection
    # Note: For explicit "safety" checks, a more advanced content moderation API or custom logic 
    # with Natural Language API's entity/syntax analysis might be needed.
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A very basic safety check: if sentiment score is very negative, flag as potentially unsafe.
    # This is a placeholder; real safety checks involve more sophisticated text analysis.
    is_safe = True
    safety_notes = []

    if sentiment.score < -0.5 and sentiment.magnitude > 1.0:
        is_safe = False
        safety_notes.append("Strongly negative sentiment detected, may require review.")

    # More robust safety checks would involve entity extraction for profanity, 
    # classification for sensitive topics, etc., which are beyond basic sentiment.
    # For demonstrative purposes, we'll keep it simple.

    return {
        "text": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_safe": is_safe,
        "safety_notes": safety_notes,
        "provider_used": "Google Cloud Natural Language API"
    }
