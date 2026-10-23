import boto3

def summarize_key_usage():
    kms_client = boto3.client('kms')

    response = kms_client.list_keys()
    keys = response['Keys']

    print("KMS Key Usage Summary:")
    print("----------------------")

    for key_metadata in keys:
        key_id = key_metadata['KeyId']
        
        try:
            key_description = kms_client.describe_key(KeyId=key_id)
            description = key_description['KeyMetadata']
            
            print(f"Key ID: {description['KeyId']}")
            print(f"  ARN: {description['Arn']}")
            print(f"  Origin: {description['Origin']}")
            print(f"  Key Usage: {description['KeyUsage']}")
            print(f"  Key State: {description['KeyState']}")
            print(f"  Creation Date: {description['CreationDate']}")
            print("---")
        except Exception as e:
            print(f"Error describing key {key_id}: {e}")
            print("---")

if __name__ == "__main__":
    summarize_key_usage()
