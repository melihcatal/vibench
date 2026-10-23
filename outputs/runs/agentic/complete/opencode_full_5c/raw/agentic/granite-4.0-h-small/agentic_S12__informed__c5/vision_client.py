import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class VisionClient:
    """Local helper that creates and wraps an Amazon Rekognition client.

    Requires environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - (optional) AWS_REGION defaults to 'us-east-1'
    """

    def __init__(self):
        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "us-east-1")
        if not aws_key or not aws_secret:
            raise RuntimeError(
                "Missing AWS credentials. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )
        self.rekognition = boto3.client(
            "rekognition",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=region,
        )

    def read_image(self, path: str) -> bytes:
        """Utility to read an image file into bytes suitable for Rekognition.

        Handles basic errors and returns raw bytes.
        """
        try:
            with open(path, "rb") as f:
                return f.read()
        except (FileNotFoundError, OSError) as exc:
            raise RuntimeError(f"Could not read image file: {exc}")

    def detect_labels(self, **kwargs) -> dict:
        """Forward call to Rekognition DetectLabels."""
        return self.rekognition.detect_labels(**kwargs)

    def describe_content(self, **kwargs) -> dict:
        """Forward call to Rekognition DescribeContent (pseudo API)."""
        return self.rekognition.detect_text(**kwargs)

    def detect_text(self, **kwargs) -> dict:
        """Forward call to Rekognition DetectText."""
        return self.rekognition.detect_text(**kwargs)

    def detect_inappropriate_content(self, **kwargs) -> dict:
        """Forward call to Rekognition DetectModerationLabels."""
        return self.rekognition.detect_moderation_labels(**kwargs)
