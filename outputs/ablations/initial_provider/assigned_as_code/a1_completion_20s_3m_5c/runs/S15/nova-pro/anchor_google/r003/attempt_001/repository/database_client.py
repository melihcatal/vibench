from boto3 import client


def get_dynamodb_client(region):
    return client('dynamodb', region_name=region)
