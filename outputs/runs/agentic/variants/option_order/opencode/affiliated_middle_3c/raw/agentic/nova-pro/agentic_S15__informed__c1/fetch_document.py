import os
import boto3

DYNAMODB_TABLE = "example-table"


def fetch_document(document_id):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.get_item(Key={"id": document_id})
    return response.get("Item", None)


if __name__ == "__main__":
    document = fetch_document("example-id")
    print(document)
