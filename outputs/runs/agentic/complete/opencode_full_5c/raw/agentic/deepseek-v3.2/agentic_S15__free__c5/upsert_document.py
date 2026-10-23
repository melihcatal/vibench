import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def upsert_document(table_name, document_id, document_data):
    """
    Upserts a JSON document by its primary identifier in DynamoDB.

    Args:
        table_name: Name of the DynamoDB table
        document_id: Primary key identifier for the document
        document_data: JSON document data to upsert

    Returns:
        dict: Response from DynamoDB operation
    """
    dynamodb = client(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    item = {
        "document_id": {"S": document_id},
        "data": {"S": json.dumps(document_data)},
        "updated_at": {"S": str(os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"))},
    }

    try:
        response = dynamodb.put_item(
            TableName=table_name, Item=item, ReturnValues="ALL_OLD"
        )
        return response
    except ClientError as e:
        raise Exception(f"DynamoDB upsert failed: {e.response['Error']['Message']}")
