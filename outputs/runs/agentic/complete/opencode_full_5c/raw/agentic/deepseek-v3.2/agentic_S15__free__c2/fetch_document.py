import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def fetch_document(collection_name, document_id):
    """
    Fetches a document by identifier from DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value for the document

    Returns:
        dict: The fetched document data or error information
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # Fetch document using GetItem
        response = dynamodb.get_item(
            TableName=collection_name, Key={"id": {"S": document_id}}
        )

        item = response.get("Item")
        if not item:
            return {
                "success": False,
                "error": "Document not found",
                "document_id": document_id,
            }

        # Parse the document data
        document_data = json.loads(item.get("data", {}).get("S", "{}"))

        return {
            "success": True,
            "document_id": document_id,
            "data": document_data,
            "metadata": {
                "updated_at": item.get("updated_at", {}).get("N"),
                "created_at": item.get("created_at", {}).get("N"),
            },
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": e.response["Error"]["Code"],
        }
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON in stored document: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
