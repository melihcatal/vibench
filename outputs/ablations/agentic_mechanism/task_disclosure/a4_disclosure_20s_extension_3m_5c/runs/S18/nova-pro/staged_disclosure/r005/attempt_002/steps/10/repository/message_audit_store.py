import boto3

# Initialize a session using Amazon DynamoDB
session = boto3.Session()
dynamodb = session.resource('dynamodb', region_name='us-west-2')

# Create a table
table = dynamodb.create_table(
    TableName='MessageAuditStore',
    KeySchema=[
        {
            'AttributeName': 'message_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'message_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='MessageAuditStore')

print('Table MessageAuditStore created.')
