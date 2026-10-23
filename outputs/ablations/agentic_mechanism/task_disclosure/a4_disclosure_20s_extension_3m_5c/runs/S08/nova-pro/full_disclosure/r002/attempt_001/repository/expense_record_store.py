import boto3

def create_expense_record_store():
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    return dynamodb

def store_expense_record(dynamodb, table_name, expense_record):
    response = dynamodb.put_item(
        TableName=table_name,
        Item=expense_record
    )
    return response