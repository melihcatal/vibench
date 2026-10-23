import boto3

def store_expense_record(normalized_expense):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ExpenseRecords')
    table.put_item(Item=normalized_expense)