import boto3


def get_cognito_client():
    config = {
        'region': 'us-west-2',
        'client_id': 'your_client_id',
        'client_secret': 'your_client_secret'
    }
    return config