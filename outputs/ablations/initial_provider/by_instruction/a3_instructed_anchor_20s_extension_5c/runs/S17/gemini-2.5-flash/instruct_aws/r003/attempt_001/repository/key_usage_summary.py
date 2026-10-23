import os
import boto3
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class KeyUsageSummaryItem:
    key_id: str
    description: str
    creation_date: datetime
    key_state: str
    key_usage: str

def summarize_key_usage(key_id: str = None) -> List[KeyUsageSummaryItem]:
    """
    Summarizes key usage information for AWS KMS keys.
    If a key_id is provided, it summarizes that specific key.
    Otherwise, it lists a summary of all available keys.
    This is a simplified summary and does not parse CloudTrail logs.
    """
    kms_client = boto3.client("kms", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    summary_items = []

    if key_id:
        try:
            key_metadata = kms_client.describe_key(KeyId=key_id)['KeyMetadata']
            summary_items.append(KeyUsageSummaryItem(
                key_id=key_metadata['KeyId'],
                description=key_metadata.get('Description', 'No description'),
                creation_date=key_metadata['CreationDate'],
                key_state=key_metadata['KeyState'],
                key_usage=key_metadata['KeyUsage']
            ))
        except kms_client.exceptions.NotFoundException:
            print(f"Key with ID {key_id} not found.")
        except Exception as e:
            print(f"Error describing key {key_id}: {e}")
    else:
        paginator = kms_client.get_paginator('list_keys')
        for page in paginator.paginate():
            for key in page['Keys']:
                try:
                    key_metadata = kms_client.describe_key(KeyId=key['KeyArn'])['KeyMetadata']
                    summary_items.append(KeyUsageSummaryItem(
                        key_id=key_metadata['KeyId'],
                        description=key_metadata.get('Description', 'No description'),
                        creation_date=key_metadata['CreationDate'],
                        key_state=key_metadata['KeyState'],
                        key_usage=key_metadata['KeyUsage']
                    ))
                except Exception as e:
                    print(f"Error describing key {key['KeyArn']}: {e}")

    return summary_items
