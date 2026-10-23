import boto3

def upsert_document(table_name, item):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response