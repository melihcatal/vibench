import boto3

def get_db_client():
    return boto3.client('dynamodb', region_name='us-west-2')