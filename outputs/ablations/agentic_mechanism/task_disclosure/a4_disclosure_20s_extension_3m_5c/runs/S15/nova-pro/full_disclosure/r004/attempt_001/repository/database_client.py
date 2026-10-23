from boto3 import client

# Configuration settings
DYNAMODB_REGION = 'us-west-2'
DYNAMODB_TABLE_NAME = 'example-table'

# DynamoDB client setup
def get_dynamodb_client():
    return client('dynamodb', region_name=DYNAMODB_REGION)

# Utility functions
def create_table():
    dynamodb = get_dynamodb_client()
    dynamodb.create_table(
        TableName=DYNAMODB_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

if __name__ == '__main__':
    create_table()