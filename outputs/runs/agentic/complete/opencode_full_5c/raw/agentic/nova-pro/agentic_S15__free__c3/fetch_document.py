import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def fetch_document(table_name, primary_key):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=primary_key)
    return response.get("Item")
