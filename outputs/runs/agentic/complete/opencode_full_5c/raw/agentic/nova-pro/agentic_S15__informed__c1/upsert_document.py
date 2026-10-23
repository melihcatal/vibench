import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upsert_document(table_name, item):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=item)
        return True
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return False
