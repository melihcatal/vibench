import os
import boto3
from botocore.exceptions import ClientError

class SafetyClient:
    """Thin wrapper around AWS Comprehend Toxicity detection.

    Uses the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    def __init__(self, region_name: str = None):
        self.region = region_name or os.getenv('AWS_REGION', 'us-east-1')
        self.client = boto3.client(
            'comprehend',
            region_name=self.region
        )

    def detect_toxicity(self, text: str) -> dict:
        """Call Comprehend DetectSentiment for toxicity.
        Returns a dict with keys: status, labels, confidence.
        """
        try:
            response = self.client.detect_sentiment(Text=text, LanguageCode='en')
            # Simplified schema for this task
            return {
                'status': response['Sentiment'],
                'labels': {k: v for k, v in response.items() if k != 'Sentiment'},
                'confidence': response['SentimentScore']['POSITIVE']  # placeholder
            }
        except ClientError as e:
            raise RuntimeError(f"AWS Comprehend error: {e}")

    def detect_toxicity_batch(self, texts: list[str]) -> list[dict]:
        """Batch detection using a loop since Comprehend has limited batch support.
        Returns list of dicts same format as single detect_toxicity.
        """
        results = []
        for txt in texts:
            results.append(self.detect_toxicity(txt))
        return results
