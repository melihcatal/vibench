import boto3
import os
from typing import List, Dict, Any
from security_models import KeyInfo

def summarize_kms_keys() -> List[KeyInfo]:
    """
    Summarizes the KMS keys available in the account and region.

    Returns:
        A list of KeyInfo objects.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    
    keys_summary: List[KeyInfo] = []
    paginator = kms_client.get_paginator('list_keys')
    
    for page in paginator.paginate():
        for key in page['Keys']:
            key_id = key['KeyId']
            # Get more details for each key
            try:
                description_response = kms_client.describe_key(KeyId=key_id)
                key_metadata = description_response['KeyMetadata']
                keys_summary.append(KeyInfo(
                    key_id=key_metadata['KeyId'],
                    arn=key_metadata['Arn'],
                    enabled=key_metadata['KeyState'] == 'Enabled',
                    description=key_metadata.get('Description')
                ))
            except Exception as e:
                print(f"Could not describe key {key_id}: {e}")
                # Append basic info if description fails
                keys_summary.append(KeyInfo(
                    key_id=key['KeyId'],
                    arn=key['KeyArn'],
                    enabled=False, # Assume disabled if cannot describe
                    description=f"Error retrieving details: {e}"
                ))
    return keys_summary

if __name__ == '__main__':
    # Example usage (requires AWS credentials)
    # export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
    # export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
    # export AWS_REGION="us-east-1"

    # print("Summarizing KMS keys...")
    # try:
    #     key_summaries = summarize_kms_keys()
    #     for key_info in key_summaries:
    #         print(f"Key ID: {key_info.key_id}")
    #         print(f"  ARN: {key_info.arn}")
    #         print(f"  Enabled: {key_info.enabled}")
    #         print(f"  Description: {key_info.description}")
    #         print("-" * 20)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
