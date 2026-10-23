import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def upsert_document(collection_name, document_id, document_data):
    """
    Upserts a JSON document by its primary identifier in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value for the document
        document_data: The JSON document data to upsert

    Returns:
        dict: Response metadata or error information
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
            "updated_at": {"N": str(int(os.time()))},
        }

        # Upsert using PutItem (overwrites if exists, creates if not)
        response = dynamodb.put_item(
            TableName=collection_name, Item=item, ReturnValues="ALL_OLD"
        )

        return {
            "success": True,
            "document_id": document_id,
            "attributes": response.get("Attributes"),
            "response_metadata": response.get("ResponseMetadata"),
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": e.response["Error"]["Code"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
