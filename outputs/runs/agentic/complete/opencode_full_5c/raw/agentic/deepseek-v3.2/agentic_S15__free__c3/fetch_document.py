import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def fetch_document(collection_name, document_id):
    """
    Fetch a document by identifier from DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value

    Returns:
        dict: Document data if found, None otherwise
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # Get item from DynamoDB
        response = dynamodb.get_item(
            TableName=collection_name, Key={"id": {"S": str(document_id)}}
        )

        # Check if item exists
        if "Item" not in response:
            return {
                "success": False,
                "error": "Document not found",
                "document_id": document_id,
                "provider": "aws:dynamodb",
            }

        item = response["Item"]

        # Parse the document data
        document_data = json.loads(item["data"]["S"])

        return {
            "success": True,
            "document_id": document_id,
            "data": document_data,
            "updated_at": item.get("updated_at", {}).get("S"),
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "document_id": document_id,
            "provider": "aws:dynamodb",
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON in stored document: {str(e)}",
            "document_id": document_id,
            "provider": "aws:dynamodb",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "document_id": document_id,
            "provider": "aws:dynamodb",
        }
