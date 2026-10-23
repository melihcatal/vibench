import boto3

# Initialize a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Name of the DynamoDB table
TABLE_NAME = 'MessageAuditStore'


def create_table():
    """Creates the DynamoDB table for message audit store"""
    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'messageId',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'messageId',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f'Table {TABLE_NAME} created successfully.')
    except dynamodb.exceptions.ResourceInUseException:
        print(f'Table {TABLE_NAME} already exists.')


def insert_message_record(message_id, message_data):
    """Inserts a message record into the DynamoDB table"""
    try:
        response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'messageId': {'S': message_id},
                'messageData': {'S': message_data}
            }
        )
        print(f'Message record with ID {message_id} inserted successfully.')
    except Exception as e:
        print(f'Error inserting message record: {e}')


def get_message_record(message_id):
    """Retrieves a message record from the DynamoDB table"""
    try:
        response = dynamodb.get_item(
            TableName=TABLE_NAME,
            Key={'messageId': {'S': message_id}}
        )
        item = response.get('Item', None)
        if item:
            print(f'Message record with ID {message_id} retrieved successfully: {item}')
        else:
            print(f'No message record found with ID {message_id}')
    except Exception as e:
        print(f'Error retrieving message record: {e}')


# Example usage
# create_table()
# insert_message_record('123', 'This is a test message')
# get_message_record('123')