import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError

def get_dynamodb_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME", "Documents"))


def upsert_document(document_id: str, document: Dict[str, Any]) -> bool:
    table = get_dynamodb_table()
    document["document_id"] = document_id
    try:
        table.put_item(Item=document)
        return True
    except ClientError as e:
        print(f"Error upserting document: {e}")
        return False