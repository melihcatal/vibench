import boto3


def fetch_document(table_name, primary_key, key_value):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={primary_key: key_value})
    return response.get("Item", None)
