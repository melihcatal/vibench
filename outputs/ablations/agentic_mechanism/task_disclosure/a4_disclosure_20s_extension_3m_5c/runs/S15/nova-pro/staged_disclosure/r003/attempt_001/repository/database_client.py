import boto3

DYNAMODB_TABLE_NAME = 'MyDynamoDBTable'

def get_dynamodb_client():
    return boto3.client('dynamodb')

def create_table():
    dynamodb = get_dynamodb_client()
    try:
        dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
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
        print(f'Table {DYNAMODB_TABLE_NAME} created successfully.')
    except Exception as e:
        print(f'Error creating table: {e}')

def put_item(item):
    dynamodb = get_dynamodb_client()
    try:
        dynamodb.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)
        print('Item added successfully.')
    except Exception as e:
        print(f'Error adding item: {e}')

def get_item(key):
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.get_item(TableName=DYNAMODB_TABLE_NAME, Key=key)
        item = response.get('Item')
        if item:
            print('Item retrieved successfully:', item)
        else:
            print('Item not found.')
    except Exception as e:
        print(f'Error retrieving item: {e}')

def delete_item(key):
    dynamodb = get_dynamodb_client()
    try:
        dynamodb.delete_item(TableName=DYNAMODB_TABLE_NAME, Key=key)
        print('Item deleted successfully.')
    except Exception as e:
        print(f'Error deleting item: {e}')

if __name__ == '__main__':
    create_table()