from typing import Dict, Any

from speech_client import get_comprehend_client
from speech_models import normalize_moderation_result

def moderate_transcript(text: str, language_code: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))

    sentiment_response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    pii_response = client.detect_pii_entities(Text=text, LanguageCode=language_code)
    
    # Combine results
    combined_result = {
        "Sentiment": sentiment_response["Sentiment"],
        "SentimentScore": sentiment_response["SentimentScore"],
        "PiiEntities": pii_response["Entities"],
    }
    
    return normalize_moderation_result(combined_result)
