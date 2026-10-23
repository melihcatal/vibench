import os
import boto3
from typing import Optional

def get_dynamodb_table(table_name: Optional[str] = None):
    table_name = table_name or os.getenv("DYNAMODB_TABLE_NAME", "documents-table")
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb.Table(table_name)