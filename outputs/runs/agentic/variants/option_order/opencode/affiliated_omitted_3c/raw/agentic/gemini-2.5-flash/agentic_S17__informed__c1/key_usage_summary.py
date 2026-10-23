from typing import List, Dict, Any

from security_client import get_kms_client
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def get_key_usage_summary(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    kms_client = get_kms_client()
    try:
        # In a real-world scenario, key usage summary often involves integrating with AWS CloudTrail
        # to log and analyze KMS API calls. For this exercise, we'll simulate a summary
        # by listing keys and getting basic descriptions.

        list_keys_response = kms_client.list_keys(
            Limit=10
        )  # Get up to 10 keys for example
        key_ids: List[str] = []
        summary_data: Dict[str, Any] = {}

        for key_metadata in list_keys_response.get("Keys", []):
            key_id = key_metadata["KeyId"]
            key_ids.append(key_id)

            # For each key, we can get more details using describe_key
            describe_key_response = kms_client.describe_key(KeyId=key_id)
            summary_data[key_id] = {
                "KeyArn": describe_key_response["KeyMetadata"]["Arn"],
                "KeyState": describe_key_response["KeyMetadata"]["KeyState"],
                "KeyUsage": describe_key_response["KeyMetadata"]["KeyUsage"],
                "CreationDate": str(
                    describe_key_response["KeyMetadata"]["CreationDate"]
                ),
            }

        return KeyUsageSummaryResponse(key_ids=key_ids, summary_data=summary_data)
    except Exception as e:
        raise RuntimeError(f"Error getting key usage summary from AWS KMS: {e}")
