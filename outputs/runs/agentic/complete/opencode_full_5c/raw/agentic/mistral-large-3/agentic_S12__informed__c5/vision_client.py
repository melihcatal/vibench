import os
from typing import Optional, Dict, Any

import boto3
from botocore.client import BaseClient


class VisionClient:
    """Client helper for Amazon Rekognition."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.client = self._create_client()

    def _create_client(self) -> BaseClient:
        """Creates a boto3 client for Amazon Rekognition."""
        return boto3.client("rekognition", region_name=self.region)

    def detect_labels(
        self, image_bytes: bytes, max_labels: int = 10, min_confidence: float = 70.0
    ) -> Dict[str, Any]:
        """Detects labels in an image."""
        return self.client.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=max_labels,
            MinConfidence=min_confidence,
        )


class AzureVisionClient:
    """Client helper for Azure AI Vision."""

    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_VISION_ENDPOINT")
        self.key = key or os.getenv("AZURE_VISION_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure AI Vision endpoint and key must be provided.")

    def get_headers(self) -> Dict[str, str]:
        """Returns headers for Azure AI Vision requests."""
        return {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/octet-stream",
        }
