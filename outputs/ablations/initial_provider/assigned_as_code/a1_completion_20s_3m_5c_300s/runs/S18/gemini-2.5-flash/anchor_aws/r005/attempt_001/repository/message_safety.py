from messaging_client import get_comprehend_client
from messaging_models import MessageSafetyResult


def check_message_safety(message_id: str, text_content: str, config=None):
    config = config or {}
    comprehend_client = get_comprehend_client(config.get("region"))
    is_safe = True
    details = {}

    try:
        # Check for sentiment (e.g., if it's overly negative, might indicate unsafe content)
        sentiment_response = comprehend_client.detect_sentiment(Text=text_content, LanguageCode="en")
        sentiment = sentiment_response["Sentiment"]
        details["sentiment"] = sentiment
        if sentiment in ["NEGATIVE", "MIXED"]:
            is_safe = False
            details["reason"] = details.get("reason", []) + ["Negative/Mixed sentiment detected"]

        # Check for PII (Personally Identifiable Information)
        pii_response = comprehend_client.detect_pii_entities(Text=text_content, LanguageCode="en")
        if pii_response["Entities"]:
            is_safe = False
            details["pii_entities_count"] = len(pii_response["Entities"])
            details["reason"] = details.get("reason", []) + ["PII detected"]

    except Exception as e:
        is_safe = False
        details["error"] = str(e)
        details["reason"] = details.get("reason", []) + ["Error during safety check"]

    return MessageSafetyResult(message_id=message_id, is_safe=is_safe, details=details)
