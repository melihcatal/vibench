import boto3

def expense_record_store(expense):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ExpenseRecords')
    table.put_item(Item=expense)