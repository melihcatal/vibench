import boto3

def store_expense_record(expense_record):
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_client.put_item(
        TableName='ExpenseRecords',
        Item=expense_record
    )