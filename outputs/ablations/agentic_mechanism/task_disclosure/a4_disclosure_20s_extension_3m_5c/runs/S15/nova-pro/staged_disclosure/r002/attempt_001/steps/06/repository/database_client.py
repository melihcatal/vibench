import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

DYNAMODB_REGION = 'us-west-2'
DYNAMODB_ACCESS_KEY = 'your_access_key'
DYNAMODB_SECRET_KEY = 'your_secret_key'

def create_dynamodb_client():
    try:
        session = boto3.Session(
            region_name=DYNAMODB_REGION,
            aws_access_key_id=DYNAMODB_ACCESS_KEY,
            aws_secret_access_key=DYNAMODB_SECRET_KEY
        )
        dynamodb_client = session.client('dynamodb')
        return dynamodb_client
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'Error creating DynamoDB client: {e}')
        return None

def list_tables(dynamodb_client):
    try:
        response = dynamodb_client.list_tables()
        return response['TableNames']
    except Exception as e:
        print(f'Error listing tables: {e}')
        return []

if __name__ == '__main__':
    dynamodb_client = create_dynamodb_client()
    if dynamodb_client:
        tables = list_tables(dynamodb_client)
        print('DynamoDB Tables:', tables)