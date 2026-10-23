import boto3



def key_usage_summary(config=None):
    config = config or {}
    client = boto3.client('kms', region_name=config.get('region'))
    response = client.list_keys()
    key_ids = [key['KeyId'] for key in response['Keys']]
    usage_summary = {}
    for key_id in key_ids:
        key_usage = client.describe_key(KeyId=key_id)
        usage_summary[key_id] = key_usage['KeyMetadata']['Description']
    return usage_summary
