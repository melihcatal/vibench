import boto3
import os
from typing import Dict, Any

def script_safety(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using AWS Comprehend.
    This implementation focuses on detecting PII and overall sentiment as proxies for safety.

    Args:
        text: The narration script text to analyze.
        language_code: The language code of the text (e.g., "en", "es").

    Returns:
        A dictionary containing analysis results, including PII detection and sentiment.
    """
    comprehend_client = boto3.client(
        'comprehend',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    # Detect PII entities
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode=language_code)
    pii_entities = pii_response.get('Entities', [])

    # Detect sentiment
    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = sentiment_response.get('Sentiment')
    sentiment_score = sentiment_response.get('SentimentScore')

    return {
        "pii_entities": pii_entities,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score
    }
