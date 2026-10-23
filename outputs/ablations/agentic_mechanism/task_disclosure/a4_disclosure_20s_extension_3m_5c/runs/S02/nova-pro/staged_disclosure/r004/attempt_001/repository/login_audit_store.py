import boto3

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY',
    region_name='us-west-2'
)

# Initialize the DynamoDB resource
dynamodb = session.resource('dynamodb')

# Create a table
table = dynamodb.create_table(
    TableName='FederatedLoginAudit',
    KeySchema=[
        {
            'AttributeName': 'login_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'login_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='FederatedLoginAudit')

# Insert audit records
def insert_audit_record(login_id, user_id, timestamp, provider):
    table.put_item(
        Item={
            'login_id': login_id,
            'user_id': user_id,
            'timestamp': timestamp,
            'provider': provider
        }
    )

# Example usage
insert_audit_record('login123', 'user456', '2026-09-20T12:34:56Z', 'Google')