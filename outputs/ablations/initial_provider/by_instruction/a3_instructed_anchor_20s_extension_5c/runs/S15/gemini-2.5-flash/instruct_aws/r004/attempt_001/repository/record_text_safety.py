import boto3
import os
from typing import Dict, Any, List
from database_models import Document

def record_text_safety(document: Document, field_to_check: str) -> Dict[str, Any]:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    comprehend = boto3.client("comprehend", region_name=aws_region)

    text_to_analyze = str(document.content.get(field_to_check, ""))

    if not text_to_analyze.strip():
        return {"status": "no_content_to_check", "findings": []}

    # Detect dominant language to ensure Comprehend works correctly
    detect_language_response = comprehend.detect_dominant_language(Text=text_to_analyze)
    dominant_language_code = detect_language_response['Languages'][0]['LanguageCode']

    # Detect PII entities
    pii_response = comprehend.detect_pii_entities(
        Text=text_to_analyze,
        LanguageCode=dominant_language_code
    )

    # Detect sentiment for general safety indication
    sentiment_response = comprehend.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode=dominant_language_code
    )
    
    # Detect a broader range of unsafe content if the language is supported by the moderation API
    # Note: AWS Comprehend's content moderation capabilities are typically through specific models or broader services like Amazon Rekognition for images and videos, 
    # or custom classification. For generic text safety, PII and sentiment analysis are good starting points within Comprehend. 
    # For more advanced content moderation, a dedicated content moderation API might be used (e.g., using a custom Comprehend classifier or Amazon Textract with custom rules).
    
    # For this example, we will focus on PII and Sentiment as indicators of potential safety concerns.

    safety_findings = {
        "pii_entities": pii_response['Entities'],
        "sentiment": sentiment_response['Sentiment'],
        "sentiment_score": sentiment_response['SentimentScore']
    }

    return {"status": "checked", "findings": safety_findings}
