import os
from typing import List

import boto3
from botocore.exceptions import ClientError


class CorpusSafetyChecker:
    """Check corpus text for toxicity using Amazon Comprehend."""

    def __init__(self):
        self.client = boto3.client(
            "comprehend",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def check_toxicity(self, text: str) -> Dict[str, Any]:
        """Check text for toxicity."""
        try:
            response = self.client.detect_toxic_content(TextSegments=[{"Text": text}])
            return {
                "toxic": any(
                    item["Score"] > 0.7 for item in response["ResultList"][0]["Labels"]
                ),
                "labels": response["ResultList"][0]["Labels"],
            }
        except ClientError as e:
            raise ValueError(f"Failed to check toxicity: {e}")

    def batch_check_toxicity(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Check a batch of texts for toxicity."""
        return [self.check_toxicity(text) for text in texts]
