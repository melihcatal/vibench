import boto3

def summarize_key_usage(key_id, region=None):
    region = region or os.getenv('AWS_REGION')
    client = boto3.client('kms', region_name=region)
    response = client.describe_key(KeyId=key_id)
    return response
