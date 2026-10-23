import boto3
from typing import Dict, Any, List
from vision_client import get_comprehend_client
from vision_models import TextSafetyRequest, TextSafetyResponse

def visual_safety_text(payload: TextSafetyRequest, config: Dict[str, Any]) -> TextSafetyResponse:
    client = get_comprehend_client(config)
    text_to_analyze = payload.text

    # Detect sentiment
    sentiment_response = client.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode='en' # Assuming English for this example
    )
    sentiment = sentiment_response.get('Sentiment')
    sentiment_score = sentiment_response.get('SentimentScore', {})

    # Detect dominant language (optional, but good practice if language is unknown)
    # dominant_language_response = client.detect_dominant_language(
    #     Text=text_to_analyze
    # )
    # dominant_language = dominant_language_response['Languages'][0]['LanguageCode']

    # Detect PII (Personally Identifiable Information) as a safety check
    # This requires a different API call and is typically for sensitive data.
    # For this exercise, we will stick to sentiment and key phrases as proxies.

    # Example logic for determining 'unsafe' based on sentiment and keywords
    is_unsafe = False
    safety_details = {
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "unsafe_keywords_detected": False,
        "unsafe_phrases": []
    }

    # A very basic example: if sentiment is negative, consider it potentially unsafe.
    # In a real scenario, a more sophisticated model or a dedicated moderation service would be used.
    if sentiment in ['NEGATIVE', 'MIXED']:
        is_unsafe = True
        
    # Additionally, check for specific unsafe keywords if provided in config
    unsafe_keywords = config.get("unsafe_text_keywords", [])
    detected_unsafe_phrases = []
    for keyword in unsafe_keywords:
        if keyword.lower() in text_to_analyze.lower():
            is_unsafe = True
            safety_details["unsafe_keywords_detected"] = True
            detected_unsafe_phrases.append(keyword)
    safety_details["unsafe_phrases"] = detected_unsafe_phrases

    return TextSafetyResponse(is_unsafe=is_unsafe, safety_details=safety_details)
