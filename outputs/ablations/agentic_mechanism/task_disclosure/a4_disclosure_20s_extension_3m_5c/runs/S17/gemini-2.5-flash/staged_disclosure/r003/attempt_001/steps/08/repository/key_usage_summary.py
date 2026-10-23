import boto3

def summarize_key_usage():
    """
    Summarizes key usage and crypto events using AWS KMS.
    This function lists all KMS keys and prints their ARN and description.
    """
    kms_client = boto3.client('kms')

    print("Listing AWS KMS keys and their descriptions:")
    try:
        paginator = kms_client.get_paginator('list_keys')
        for page in paginator.paginate():
            for key in page['Keys']:
                key_id = key['KeyId']
                # Describe the key to get more details, including description
                key_metadata = kms_client.describe_key(KeyId=key_id)['KeyMetadata']
                print(f"  Key ARN: {key_metadata['Arn']}")
                print(f"  Description: {key_metadata.get('Description', 'No description provided')}")
                print(f"  Key State: {key_metadata['KeyState']}")
                print("-" * 20)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    summarize_key_usage()
