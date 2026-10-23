# [HELPER] observability_client.py
import os
import boto3
from typing import Any, Dict, Optional

class Boto3Client:
    """Thin wrapper providing a unified SDK interface for AWS services.
    Currently used for CloudWatch Metrics; can be extended for other AWS services.
    """
    def __init__(self, service: str, region_name: Optional[str] = None):
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.client = boto3.client(
            service,
            region_name=region_name or "us-east-1",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
    def get_metric_statistics(self, request: Any) -> Any:
        # Convert request model to dict expected by boto3
        kwargs = request.dict(exclude_none=True)
        # Boto3 expects period as integer without 'period=' prefix
        return self.client.get_metric_statistics(**kwargs)
