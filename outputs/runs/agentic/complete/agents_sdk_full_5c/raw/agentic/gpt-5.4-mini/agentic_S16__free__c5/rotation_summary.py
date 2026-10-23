import os
from typing import Dict, Optional

from security_client import get_secret_manager_client
from security_models import SecretFetchRequest

# AWS Secrets Manager provider signal
import boto3


def rotation_summary(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, str]:
    region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    client = get_secret_manager_client(provider="aws", region_name=region)
    request = SecretFetchRequest(secret_name=secret_id or os.getenv("ROTATION_SECRET_ID", "rotation-status"), version="AWSCURRENT")
    result = client.describe_secret(SecretId=request.secret_name)
    last_changed = result.get("LastChangedDate")
    rotation_enabled = result.get("RotationEnabled")
    return {"secret_name": request.secret_name, "rotation_enabled": str(bool(rotation_enabled)), "last_changed": str(last_changed)}
