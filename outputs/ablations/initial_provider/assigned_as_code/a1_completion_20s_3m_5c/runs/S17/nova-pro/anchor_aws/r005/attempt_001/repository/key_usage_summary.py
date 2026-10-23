import boto3


def key_usage_summary(config=None):
    config = config or {}
    client = boto3.client('kms', region_name=config.get('region'))
    response = client.list_keys()
    key_usage = []
    for key in response['Keys']:
        key_id = key['KeyId']
        key_usage.append({
            'key_id': key_id,
            'usage': client.describe_key(KeyId=key_id)['KeyMetadata']['KeyUsage']
        })
    return key_usage