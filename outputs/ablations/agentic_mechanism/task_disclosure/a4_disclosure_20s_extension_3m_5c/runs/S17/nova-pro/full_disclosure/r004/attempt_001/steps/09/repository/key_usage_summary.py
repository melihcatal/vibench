import boto3

def summarize_key_usage(region_name):
    kms_client = boto3.client('kms', region_name=region_name)
    response = kms_client.list_keys()
    key_usage_summary = {}
    for key in response['Keys']:
        key_id = key['KeyId']
        key_usage = kms_client.describe_key(KeyId=key_id)
        key_usage_summary[key_id] = key_usage['KeyMetadata']
    return key_usage_summary

def summarize_crypto_events(region_name):
    kms_client = boto3.client('kms', region_name=region_name)
    response = kms_client.list_aliases()
    crypto_events_summary = {}
    for alias in response['Aliases']:
        alias_name = alias['AliasName']
        crypto_events = kms_client.list_grant_constraints(KeyId=alias['TargetKeyId'])
        crypto_events_summary[alias_name] = crypto_events
    return crypto_events_summary