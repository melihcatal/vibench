import os
import boto3

from messaging_models import Message

def check_message_safety(message: Message, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    language_code = config.get("language_code", "en")

    comprehend_client = boto3.client("comprehend", region_name=region_name)

    text_to_analyze = str(message.payload) # Convert payload to string for analysis

    # Detect dominant language if not provided
    if language_code == "auto":
        detect_language_response = comprehend_client.detect_dominant_language(Text=text_to_analyze)
        dominant_language = detect_language_response['Languages'][0]['LanguageCode']
        language_code = dominant_language

    # Detect sentiment for general safety check
    sentiment_response = comprehend_client.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode=language_code
    )

    # Detect entities for potential unsafe content (e.g., PII, medical info, etc.)
    # This part can be extended based on specific safety requirements.
    entities_response = comprehend_client.detect_entities(
        Text=text_to_analyze,
        LanguageCode=language_code
    )

    is_safe = True
    safety_concerns = []

    if sentiment_response['Sentiment'] in ['NEGATIVE', 'MIXED']:
        is_safe = False
        safety_concerns.append(f"Negative/Mixed sentiment detected: {sentiment_response['Sentiment']}")

    # Example of checking for specific entity types that might indicate unsafe content
    # This is a simplified example; a real-world scenario would have more complex rules.
    for entity in entities_response['Entities']:
        if entity['Type'] in ['PII', 'MEDICAL_CONDITION', 'PERSONAL_IDENTIFICATION_NUMBER']:
            is_safe = False
            safety_concerns.append(f"Potentially sensitive entity detected: {entity['Type']} - {entity['Text']}")

    return {
        "message_id": message.message_id,
        "is_safe": is_safe,
        "safety_concerns": safety_concerns,
        "sentiment": sentiment_response['Sentiment']
    }
