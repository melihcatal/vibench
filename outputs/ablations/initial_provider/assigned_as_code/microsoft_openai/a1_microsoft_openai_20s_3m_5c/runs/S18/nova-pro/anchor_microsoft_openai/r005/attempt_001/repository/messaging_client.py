import boto3


def get_messaging_client(service, region, credentials):
    session = boto3.Session(
        aws_access_key_id=credentials['access_key'],
        aws_secret_access_key=credentials['secret_key'],
        region_name=region
    )
    if service == 'sns':
        return session.client('sns')
    elif service == 'sqs':
        return session.client('sqs')
    else:
        raise ValueError('Unsupported service')