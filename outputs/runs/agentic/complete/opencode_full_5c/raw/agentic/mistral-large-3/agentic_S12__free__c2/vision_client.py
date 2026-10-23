import os
from typing import List, Dict, Optional
import boto3
from botocore.exceptions import ClientError


class AWSVisionClient:
    """Client helper for AWS Rekognition service."""

    def __init__(self):
        self.client = boto3.client(
            "rekognition",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def detect_labels(self, image_bytes: bytes, max_labels: int = 10) -> Dict:
        """Detect labels in an image using AWS Rekognition."""
        try:
            response = self.client.detect_labels(
                Image={"Bytes": image_bytes}, MaxLabels=max_labels, MinConfidence=70.0
            )
            return response
        except ClientError as e:
            raise Exception(f"AWS Rekognition error: {e}")

    def detect_text(self, image_bytes: bytes) -> Dict:
        """Detect text in an image using AWS Rekognition."""
        try:
            response = self.client.detect_text(Image={"Bytes": image_bytes})
            return response
        except ClientError as e:
            raise Exception(f"AWS Rekognition error: {e}")

    def detect_moderation_labels(self, image_bytes: bytes) -> Dict:
        """Detect moderation labels in an image using AWS Rekognition."""
        try:
            response = self.client.detect_moderation_labels(
                Image={"Bytes": image_bytes}, MinConfidence=70.0
            )
            return response
        except ClientError as e:
            raise Exception(f"AWS Rekognition error: {e}")

    def generate_image_description(self, image_bytes: bytes) -> Optional[str]:
        """Generate a description for an image using AWS Rekognition labels."""
        labels_response = self.detect_labels(image_bytes, max_labels=10)
        labels = [label["Name"] for label in labels_response.get("Labels", [])]
        if not labels:
            return None
        return ", ".join(labels)
