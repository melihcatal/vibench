import os
import json
from typing import Any, Dict

# Local configuration and AWS credentials handling
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


# Helper to create a Secrets Manager client with region configuration
def create_secrets_manager_client() -> Any:
    """Create and return a configured boto3 Secrets Manager client."""
    return boto3.client("secretsmanager", region_name=AWS_REGION)


# Payload normalization utilities
def normalize_secret_response(response: dict) -> Dict[str, Any]:
    """Normalize AWS Secrets Manager response into a consistent dict."""
    secret = response.get("SecretString")
    if not secret:
        raise ValueError("Secret string not found in response")
    return json.loads(secret)
