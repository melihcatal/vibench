import os

import boto3


def profile_note_store(note: dict):
    dynamodb = boto3.resource(
        "dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])
    table.put_item(Item=note)
    return {"stored": True, "provider": "Amazon DynamoDB"}
