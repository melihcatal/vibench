import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ExpenseRecords')

def store_expense_record(record):
    table.put_item(Item=record)