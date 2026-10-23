import json

from security_client import get_comprehend_client
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    comprehend_client = get_comprehend_client()
    safety_details = {}
    is_safe = True

    try:
        # Amazon Comprehend provides various NLP functionalities. For 'toxicity' detection,
        # a direct API like 'detect_toxic_content' isn't explicitly available in the main Comprehend client.
        # However, we can use other APIs as proxies for general content safety or integrate with
        # AWS Bedrock Guardrails or Amazon Textract/Rekognition for more comprehensive content moderation.
        # For this exercise, we will use sentiment and dominant language detection as a general indicator.
        # In a real-world scenario, for explicit toxicity, you would integrate with services like
        # Amazon Rekognition (for images/videos) or custom ML models.

        # Detect dominant language
        language_response = comprehend_client.detect_dominant_language(
            Text=request.text
        )
        dominant_language = (
            language_response["Languages"][0]["LanguageCode"]
            if language_response["Languages"]
            else "unknown"
        )
        safety_details["dominant_language"] = dominant_language

        # Detect sentiment
        sentiment_response = comprehend_client.detect_sentiment(
            Text=request.text, LanguageCode=dominant_language
        )
        sentiment = sentiment_response["Sentiment"]
        safety_details["sentiment"] = sentiment
        safety_details["sentiment_scores"] = sentiment_response["SentimentScore"]

        # A very basic safety check: if sentiment is overwhelmingly negative, might flag as less safe
        if (
            sentiment == "NEGATIVE"
            and sentiment_response["SentimentScore"]["Negative"] > 0.8
        ):
            is_safe = False
            safety_details["reason"] = "Overwhelmingly negative sentiment detected."

        # Placeholder for more explicit toxicity/safety checks with other services if available
        # E.g., integration with Amazon Bedrock Guardrails or a custom content moderation solution.

        return PayloadSafetyResponse(is_safe=is_safe, details=safety_details)
    except Exception as e:
        raise RuntimeError(f"Error checking payload safety with Amazon Comprehend: {e}")
