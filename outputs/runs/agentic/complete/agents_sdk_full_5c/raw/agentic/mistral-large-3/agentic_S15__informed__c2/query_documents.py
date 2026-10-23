import os
from typing import Dict, Any, List
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


def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    table = get_dynamodb_table()
    try:
        response = table.query(
            IndexName=f"{field_name}-index" if field_name != "document_id" else None,
            KeyConditionExpression=boto3.dynamodb.conditions.Key(field_name).eq(field_value)
        )
        return response.get("Items", [])
    except ClientError as e:
        print(f"Error querying documents: {e}")
        return []