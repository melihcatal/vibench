import boto3

def summarize_key_usage():
    kms_client = boto3.client('kms')
    key_usage_metrics = kms_client.get_key_rotation_status(KeyId='alias/example_key')
    crypto_events = kms_client.list_aliases()
    
    print('Key Usage Metrics:', key_usage_metrics)
    print('Crypto Events:', crypto_events)

if __name__ == '__main__':
    summarize_key_usage()