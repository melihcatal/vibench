import os
import json
from typing import Any, Dict
from security_client import get_aws_kms_client

# Configure KMS client using AWS credentials
_kms_client = get_aws_kms_client()


def key_usage_summary() -> Dict[str, Any]:
    """Summarize recent key usage events from AWS KMS for the configured key.

    This helper demonstrates how you could query CloudTrail or KMS metrics and
    return a concise JSON summary for downstream processes (e.g., central dashboard).
    """
    key_id = os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise RuntimeError("AWS_KMS_KEY_ID not set")
    # Placeholder: in a real implementation call CloudWatch Logs Insights or CloudTrail
    # to retrieve counts of Encrypt/Decrypt calls over the last 24h
    summary = {
        "KeyId": key_id,
        "Region": os.getenv("AWS_REGION", "us-east-1"),
        "TotalEncryptions": 0,
        "TotalDecryptions": 0,
        "LastEventTimestamp": None,
    }
    # NOTE: In production replace this with an actual API call and populate fields
    return summary


if __name__ == "__main__":
    print(json.dumps(key_usage_summary(), indent=2))
