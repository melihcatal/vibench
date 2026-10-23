import boto3
import os

def moderate_text_with_aws_comprehend(text: str, language_code: str = "en"):
    """
    Moderates transcript text using AWS Comprehend for sentiment and PII detection.
    """
    comprehend_client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode=language_code)
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode=language_code)

    return {
        "sentiment": sentiment_response,
        "pii_entities": pii_response
    }
