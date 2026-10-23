import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def upsert_document(collection_name, document_id, document_data):
    """
    Upsert a JSON document by its primary identifier in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value
        document_data: The JSON document data to upsert

    Returns:
        dict: Result containing success status and metadata
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # Prepare the item for DynamoDB
        item = {
            "id": {"S": str(document_id)},
            "data": {"S": json.dumps(document_data)},
            "updated_at": {
                "S": str(os.environ.get("TIMESTAMP", "2025-01-01T00:00:00Z"))
            },
        }

        # Upsert using PutItem (overwrites if exists)
        response = dynamodb.put_item(
            TableName=collection_name, Item=item, ReturnValues="ALL_OLD"
        )

        # Check if item existed before
        was_updated = "Attributes" in response

        return {
            "success": True,
            "document_id": document_id,
            "was_updated": was_updated,
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "aws:dynamodb",
            "document_id": document_id,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "provider": "aws:dynamodb",
            "document_id": document_id,
        }
