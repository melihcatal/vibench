import os
import boto3
from typing import Dict, Any, List

def check_annotation_safety(text: str) -> Dict[str, Any]:
    """
    Checks free-text metric labels or annotations for unsafe text using AWS Comprehend.
    """
    comprehend = boto3.client('comprehend', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        response = comprehend.detect_dominant_language(Text=text)
        dominant_language_code = "en" # Default to English
        if response and response.get('Languages'):
            dominant_language_code = response['Languages'][0]['LanguageCode']

        pii_entities_response = comprehend.detect_pii_entities(
            Text=text,
            LanguageCode=dominant_language_code
        )

        sentiment_response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode=dominant_language_code
        )

        return {
            "text": text,
            "dominant_language": dominant_language_code,
            "pii_entities": pii_entities_response.get('Entities', []),
            "sentiment": sentiment_response.get('Sentiment', 'NEUTRAL'),
            "sentiment_scores": sentiment_response.get('SentimentScore', {}),
        }

    except Exception as e:
        return {"error": str(e)}
