import boto3

DYNAMODB_TABLE = 'ExpenseRecords'

def get_dynamodb_client():
    return boto3.client('dynamodb')

def store_expense_record(record):
    client = get_dynamodb_client()
    response = client.put_item(
        TableName=DYNAMODB_TABLE,
        Item=record
    )
    return response