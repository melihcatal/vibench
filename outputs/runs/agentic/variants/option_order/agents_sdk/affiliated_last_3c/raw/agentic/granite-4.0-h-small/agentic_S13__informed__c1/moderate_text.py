import os
from safety_client import SafetyClient

def moderate_text(user_text: str) -> dict:
    """Send a single text to the safety provider and return moderation result.

    The provider used is Amazon Comprehend Toxicity (AWS Comprehend)
    identified by the boto3 client and the AWS credentials in the environment.
    """
    client = SafetyClient()
    response = client.detect_toxicity(text=user_text)
    # response format mimics Amazon Comprehend's output
    return {
        "status": response.get('status'),
        "labels": response.get('labels'),
        "confidence": response.get('confidence')
    }
