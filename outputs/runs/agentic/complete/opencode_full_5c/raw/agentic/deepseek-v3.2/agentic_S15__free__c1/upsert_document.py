import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def upsert_document(collection_name, document_id, document_data):
    """
    Upserts a JSON document by its primary identifier into DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key identifier
        document_data: JSON document data to upsert

    Returns:
        dict: Operation result with status and metadata
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
            "id": {"S": document_id},
            "data": {"S": json.dumps(document_data)},
            "updated_at": {"S": "2025-04-18T12:00:00Z"},  # Simplified timestamp
        }

        # Upsert using PutItem (overwrites if exists, creates if not)
        response = dynamodb.put_item(
            TableName=collection_name, Item=item, ReturnValues="ALL_OLD"
        )

        # Check if item was created or updated
        was_created = "Attributes" not in response or not response["Attributes"]

        return {
            "success": True,
            "document_id": document_id,
            "operation": "created" if was_created else "updated",
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "aws:dynamodb",
            "operation": "upsert",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "aws:dynamodb",
            "operation": "upsert",
        }
