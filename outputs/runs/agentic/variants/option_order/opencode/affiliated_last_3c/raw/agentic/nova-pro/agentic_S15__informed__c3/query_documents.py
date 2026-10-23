import boto3


def query_documents(table_name, key_condition):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=key_condition)
    return response.get("Items")
