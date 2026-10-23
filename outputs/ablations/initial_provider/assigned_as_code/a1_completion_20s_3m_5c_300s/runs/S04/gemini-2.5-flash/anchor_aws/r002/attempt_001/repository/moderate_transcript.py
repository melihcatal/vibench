from speech_client import SpeechClient
from speech_models import ModerateRequest


def moderate_transcript(request: ModerateRequest, config=None) -> dict:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_comprehend_client()

    # For content moderation, we can use detect_sentiment or detect_dominant_language
    # or custom classification if trained. For a general moderation, 
    # we will use detect_sentiment and detect_pii_entities as an example.

    sentiment_response = client.detect_sentiment(
        Text=request.text,
        LanguageCode=request.language_code
    )

    pii_response = client.detect_pii_entities(
        Text=request.text,
        LanguageCode=request.language_code
    )

    return {
        "sentiment": sentiment_response["Sentiment"],
        "sentiment_scores": sentiment_response["SentimentScore"],
        "pii_entities": pii_response["Entities"],
    }
