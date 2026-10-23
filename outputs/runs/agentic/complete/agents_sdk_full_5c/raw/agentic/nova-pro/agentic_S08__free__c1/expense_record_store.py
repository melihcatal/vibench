import boto3

def store_expense_record(expense_record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ExpenseRecords')
    table.put_item(Item=expense_record)
    # Storage logic here