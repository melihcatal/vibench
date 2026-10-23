import os
import boto3


def fetch_document(identifier: str):
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    client = boto3.client("dynamodb", region_name=region)
    response = client.get_item(
        TableName=table_name,
        Key={"id": {"S": identifier}},
        ConsistentRead=True,
    )
    return response.get("Item")
