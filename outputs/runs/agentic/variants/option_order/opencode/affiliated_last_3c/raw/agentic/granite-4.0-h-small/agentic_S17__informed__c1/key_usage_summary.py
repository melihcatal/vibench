import os
import boto3
from typing import Any, Dict, List

# AWS KMS integration – uses the AWS Key Management Service
# Provider identifiable by boto3 import and client creation

kms = boto3.client(
    "kms",
    # Credentials read from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
)


def fetch_key_metrics(key_id: str) -> Dict[str, Any]:
    """
    Retrieve usage metrics for a single KMS key.
    The AWS API returns certain metrics like NumberOfUses, LastUse, etc.
    """
    response = kms.describe_key(KeyId=key_id)
    # The DescribeKey response includes a few usage-related fields
    key_metadata = response["KeyMetadata"]
    return {
        "KeyId": key_id,
        "Arn": key_metadata.get("Arn"),
        "CreationDate": key_metadata.get("CreationDate"),
        "Enabled": key_metadata.get("Enabled"),
        "Description": key_metadata.get("Description"),
        "NumberOfUses": key_metadata.get(
            "NumberOfUses"
        ),  # may be omitted if not tracked
    }


def summarize_usage(key_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Given a list of KMS key identifiers, return a summary list with basic metadata
    and usage information.
    """
    summaries = []
    for kid in key_ids:
        try:
            metrics = fetch_key_metrics(kid)
            summaries.append(metrics)
        except Exception as e:
            # Log and continue – some keys may not expose usage fields
            print(f"Failed to fetch usage for {kid}: {e}")
    return summaries


# Example usage (uncomment for local testing)
# if __name__ == '__main__':
#     key_list = ['alias/my-key-1', 'key/1234abcd-12ab-34cd-56ef-1234567890ab']
#     for entry in summarize_usage(key_list):
#         print(entry)
