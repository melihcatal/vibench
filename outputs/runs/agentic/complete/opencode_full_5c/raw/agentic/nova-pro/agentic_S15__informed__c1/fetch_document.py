import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def fetch_document(table_name, key):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key=key)
        return response.get("Item")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return None
