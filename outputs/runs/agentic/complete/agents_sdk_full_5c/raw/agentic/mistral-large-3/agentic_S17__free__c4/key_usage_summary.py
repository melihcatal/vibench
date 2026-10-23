import os
from datetime import datetime, timedelta
from security_client import get_kms_client
import pandas as pd


def summarize_key_usage(key_id: str, days: int = 7) -> dict:
    client = get_kms_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    
    # Fetch AWS CloudTrail logs via AWS KMS API (simplified for example)
    # In practice, use AWS CloudTrail or AWS KMS metrics
    response = client.get_key_rotation_status(KeyId=key_id)
    
    # Mock usage data for demonstration
    usage_data = {
        "KeyId": key_id,
        "EncryptOperations": _mock_operation_count("encrypt"),
        "DecryptOperations": _mock_operation_count("decrypt"),
        "SignOperations": _mock_operation_count("sign"),
        "VerifyOperations": _mock_operation_count("verify"),
        "LastRotated": response.get("KeyRotationEnabled", False),
        "PeriodStart": start_time.isoformat(),
        "PeriodEnd": end_time.isoformat()
    }
    
    return usage_data


def _mock_operation_count(operation: str) -> int:
    # In practice, query AWS CloudWatch or CloudTrail
    return 42  # Mock value