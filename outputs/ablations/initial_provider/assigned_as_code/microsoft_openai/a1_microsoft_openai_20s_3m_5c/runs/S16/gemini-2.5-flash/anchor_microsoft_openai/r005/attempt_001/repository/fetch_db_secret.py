import os
import boto3

def fetch_db_secret(payload, config=None):
    config = config or {}
    secret_name = payload['secret_id']
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = get_secret_value_response['SecretBinary'].decode('utf-8')

    return {'db_secret': secret}
