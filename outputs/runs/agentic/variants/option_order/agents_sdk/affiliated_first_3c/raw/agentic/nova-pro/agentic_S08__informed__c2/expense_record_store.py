import boto3

def expense_record_store(record):
    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.put_item(TableName='ExpenseRecords', Item=record)
    return response