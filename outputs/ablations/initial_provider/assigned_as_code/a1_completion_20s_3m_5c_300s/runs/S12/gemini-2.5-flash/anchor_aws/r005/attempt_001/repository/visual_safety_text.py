from vision_client import get_comprehend_client


def visual_safety_text(payload, config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))

    text_to_analyze = payload.get("text", "")
    
    if not text_to_analyze:
        return {"safety_score": {"overall_sentiment": "NEUTRAL", "sentiment_scores": {}}}

    # Using detect_sentiment as a proxy for text safety. 
    # A more robust solution might involve custom Comprehend models or other services.
    response = client.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode=config.get("language_code", "en")
    )

    return {
        "safety_score": {
            "overall_sentiment": response["Sentiment"],
            "sentiment_scores": response["SentimentScore"]
        }
    }
