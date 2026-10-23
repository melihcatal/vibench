import boto3

# Initialize a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name
table_name = 'FederatedLoginAudit'

# Create the DynamoDB table
try:
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'audit_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'audit_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print(f'Table {table_name} created successfully') 
except dynamodb.exceptions.ResourceInUseException:
    print(f'Table {table_name} already exists')

# Function to persist audit records
def persist_audit_record(audit_id, audit_data):
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item={'audit_id': {'S': audit_id}, 'audit_data': {'S': audit_data}}
        )
        print(f'Audit record with ID {audit_id} persisted successfully')
    except Exception as e:
        print(f'Error persisting audit record: {e}')

# Example usage
persist_audit_record('audit-123', 'User logged in successfully')