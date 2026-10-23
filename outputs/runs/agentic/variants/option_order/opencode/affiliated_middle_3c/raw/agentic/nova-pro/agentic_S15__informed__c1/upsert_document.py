import os
import boto3

DYNAMODB_TABLE = "example-table"


def upsert_document(document_id, document):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.put_item(Item={"id": document_id, **document})


if __name__ == "__main__":
    example_document = {"name": "example", "value": 123}
    upsert_document("example-id", example_document)
