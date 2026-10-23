import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name
table_name = 'ExpenseRecords'


def store_expense_record(record):
    '''
    Store a normalized expense record in DynamoDB.
    
    Args:
        record (dict): The expense record to store.
    '
    response = dynamodb.put_item(
        TableName=table_name,
        Item=record
    )
    return response
