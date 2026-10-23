import boto3
import os
from typing import List, Dict, Any

def moderate_claims(text: str, language_code: str = "en") -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        # Detect PII entities
        pii_response = client.detect_pii_entities(Text=text, LanguageCode=language_code)
        
        # Detect sentiment
        sentiment_response = client.detect_sentiment(Text=text, LanguageCode=language_code)
        
        # Detect key phrases
        key_phrases_response = client.detect_key_phrases(Text=text, LanguageCode=language_code)

        return {
            "pii_entities": pii_response["Entities"],
            "sentiment": sentiment_response["Sentiment"],
            "sentiment_score": sentiment_response["SentimentScore"],
            "key_phrases": [phrase["Text"] for phrase in key_phrases_response["KeyPhrases"]]
        }
    except Exception as e:
        raise RuntimeError(f"Error moderating claims with AWS Comprehend: {e}")
