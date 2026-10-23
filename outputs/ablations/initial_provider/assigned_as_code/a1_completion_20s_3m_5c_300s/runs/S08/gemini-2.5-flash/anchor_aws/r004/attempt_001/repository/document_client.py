import os
import boto3
from typing import Dict, Any

def get_aws_client(service_name: str, region_name: str = None):
    """Provides a configured AWS client for a given service."""
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = region_name or os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            service_name,
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    else:
        # Fallback to default AWS credential chain (e.g., IAM roles, ~/.aws/credentials)
        return boto3.client(service_name, region_name=aws_region)


def load_config() -> Dict[str, Any]:
    """Loads configuration from environment variables or a default.
    For a real application, this would load from a more robust config management system.
    """
    return {
        "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
        "textract_feature_types": ["FORMS", "TABLES"], # Example feature types
    }
