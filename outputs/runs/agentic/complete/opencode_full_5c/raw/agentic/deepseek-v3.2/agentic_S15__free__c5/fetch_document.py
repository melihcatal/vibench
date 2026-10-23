import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def fetch_document(table_name, document_id):
    """
    Fetches a document by identifier from DynamoDB.

    Args:
        table_name: Name of the DynamoDB table
        document_id: Primary key identifier for the document

    Returns:
        dict: Document data if found, None otherwise
    """
    dynamodb = client(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = dynamodb.get_item(
            TableName=table_name, Key={"document_id": {"S": document_id}}
        )

        if "Item" in response:
            item = response["Item"]
            if "data" in item:
                return json.loads(item["data"]["S"])
        return None
    except ClientError as e:
        raise Exception(f"DynamoDB fetch failed: {e.response['Error']['Message']}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse document data: {str(e)}")
