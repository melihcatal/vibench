import boto3
from typing import Dict

from safety_client import get_aws_credentials
from safety_models import ModerationResult, SafetyRating

def check_text_with_thresholds(text: str, thresholds: Dict[str, float]) -> bool:
    """
    Checks if text toxicity scores from Amazon Comprehend exceed given thresholds.
    Returns True if the text is allowed (below thresholds), False otherwise.
    """
    get_aws_credentials()  # Ensures credentials are loaded from env
    client = boto3.client(service_name='comprehend')

    try:
        response = client.detect_toxic_content(
            TextSegments=[{'Text': text}],
            LanguageCode='en'
        )
    except Exception as e:
        print(f"Error calling Amazon Comprehend: {e}")
        # Fail safe: if the check fails, assume the content is unsafe.
        return False
        
    if not response.get('ResultList'):
        return True # No toxicity detected

    toxicity_scores = {
        label['Name']: label['Score']
        for label in response['ResultList'][0]['Labels']
    }

    for category, threshold in thresholds.items():
        if toxicity_scores.get(category, 0.0) > threshold:
            return False  # Block if any category exceeds its threshold

    return True  # Allow if all scores are within thresholds
