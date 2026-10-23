import os
import json
from typing import Dict, Any
import boto3
from messaging_models import PubsubMessage

def check_message_safety(message: PubsubMessage) -> Dict[str, Any]:
    """Checks the safety of the message payload text using AWS Comprehend.
    Specifically, it checks for sentiment, which can indicate potentially unsafe or negative content.

    Args:
        message: The PubsubMessage object containing the payload to check.

    Returns:
        A dictionary containing the sentiment analysis results from AWS Comprehend.
    """
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Assuming the main text content is in the 'data' part of the PubsubMessage
    # You might need to adjust this based on your specific message structure
    text_to_analyze = json.dumps(message.data) if isinstance(message.data, dict) else str(message.data)

    if not text_to_analyze.strip():
        return {"sentiment": "NEUTRAL", "sentiment_score": {"Neutral": 1.0}, "message": "No text to analyze"}

    response = comprehend_client.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode="en" # Assuming English for this example, can be dynamic
    )
    return response

if __name__ == '__main__':
    # Example usage
    safe_message = PubsubMessage(
        message_id="msg-safe",
        data={"text": "This is a wonderful product and I am very happy!"},
        attributes={'type': 'review'}
    )

    unsafe_message = PubsubMessage(
        message_id="msg-unsafe",
        data={"text": "I hate this product, it's terrible and a waste of money."},
        attributes={'type': 'review'}
    )
    
    empty_message = PubsubMessage(
        message_id="msg-empty",
        data={'text': ''},
        attributes={'type': 'review'}
    )

    print("Checking safe message:")
    safe_result = check_message_safety(safe_message)
    print(json.dumps(safe_result, indent=2))

    print("\nChecking unsafe message:")
    unsafe_result = check_message_safety(unsafe_message)
    print(json.dumps(unsafe_result, indent=2))

    print("\nChecking empty message:")
    empty_result = check_message_safety(empty_message)
    print(json.dumps(empty_result, indent=2))
