import boto3
import os
import json

def check_safety(text: str) -> dict:
    """
    Checks the given text for unsafe content using AWS Comprehend.
    """
    comprehend = boto3.client(
        service_name='comprehend',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    # Example: Detect sentiment (can be extended for more specific content moderation)
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    # For more advanced content moderation, you would typically use a specialized moderation API
    # or a combination of services. Comprehend can do PII, entities, key phrases, etc.
    # This example demonstrates a basic integration with Comprehend.

    return {
        "sentiment": response['Sentiment'],
        "sentiment_score": response['SentimentScore'],
        "raw_comprehend_response": response
    }
