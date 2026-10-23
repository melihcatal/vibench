from speech_client import get_comprehend_client


def script_safety(text, language_code="en", config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))
    
    # Detect sentiment to infer safety/toxicity (basic example)
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = sentiment_response['Sentiment']
    sentiment_score = sentiment_response['SentimentScore']
    
    # More advanced safety checks would involve custom models or deeper analysis
    is_safe = True if sentiment in ['NEUTRAL', 'POSITIVE'] else False # Simple heuristic

    return {
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "is_safe": is_safe
    }
