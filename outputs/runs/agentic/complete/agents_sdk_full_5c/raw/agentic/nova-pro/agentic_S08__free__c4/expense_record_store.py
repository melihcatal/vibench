import boto3

dynamodb_client = boto3.client('dynamodb')

def store_expense_record(expense):
    dynamodb_client.put_item(
        TableName='ExpenseRecords',
        Item=expense)