import os
from typing import Dict, Any, Optional
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


def fetch_document(document_id: str) -> Optional[Dict[str, Any]]:
    table = get_dynamodb_table()
    try:
        response = table.get_item(Key={"document_id": document_id})
        return response.get("Item")
    except ClientError as e:
        print(f"Error fetching document: {e}")
        return None