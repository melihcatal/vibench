import boto3

dynamodb = boto3.client('dynamodb')

def upsert_document(table_name, item):
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response