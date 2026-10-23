"""Local configuration and client helper utilities for AWS S3 Managed Object Storage."""

import os
import boto3
from botocore.config import Config
from typing import Optional


class S3ClientFactory:
    """Factory for creating pre-configured AWS S3 and related service clients."""

    DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    DEFAULT_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", None)
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "managed-storage-bucket")

    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        bucket: Optional[str] = None,
    ):
        self.region = region or self.DEFAULT_REGION
        self.endpoint_url = endpoint_url or self.DEFAULT_ENDPOINT_URL
        self.bucket = bucket or self.S3_BUCKET

        retry_config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
            connect_timeout=10,
            read_timeout=30,
        )

        session_kwargs = {"region_name": self.region}
        if self.endpoint_url:
            session_kwargs["endpoint_url"] = self.endpoint_url

        self._s3_client = boto3.client("s3", config=retry_config, **session_kwargs)
        self._s3_resource = boto3.resource("s3", config=retry_config, **session_kwargs)

    @property
    def s3_client(self):
        """Return the raw boto3 S3 client."""
        return self._s3_client

    @property
    def s3_resource(self):
        """Return the boto3 S3 resource."""
        return self._s3_resource

    def get_textract_client(self):
        """Return a boto3 Textract client for OCR operations."""
        return boto3.client("textract", region_name=self.region)

    def get_translate_client(self):
        """Return a boto3 Translate client for text translation."""
        return boto3.client("translate", region_name=self.region)

    def get_bedrock_runtime_client(self):
        """Return a boto3 Bedrock Runtime client for AI inference."""
        return boto3.client("bedrock-runtime", region_name=self.region)

    def validate_bucket_exists(self) -> bool:
        """Check if the configured S3 bucket exists and is accessible."""
        try:
            self._s3_client.head_bucket(Bucket=self.bucket)
            return True
        except self._s3_client.exceptions.ClientError:
            return False

    def get_bucket_location(self) -> str:
        """Retrieve the AWS region where the bucket resides."""
        response = self._s3_client.get_bucket_location(Bucket=self.bucket)
        return response.get("LocationConstraint") or self.region
