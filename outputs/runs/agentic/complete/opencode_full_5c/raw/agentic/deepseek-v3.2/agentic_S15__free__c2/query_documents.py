import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def query_documents(collection_name, field_name, field_value, limit=100):
    """
    Queries documents by a field value in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        field_name: The field name to query on
        field_value: The field value to match
        limit: Maximum number of documents to return

    Returns:
        dict: Query results or error information
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # For DynamoDB, we need to use a GSI or scan with filter
        # This example uses a scan with filter expression (for simplicity)
        # In production, you would use a GSI for efficient queries

        filter_expression = f"contains(#data, :value)"
        expression_attribute_names = {"#data": "data"}
        expression_attribute_values = {
            ":value": {"S": f'"{field_name}":"{field_value}"'}
        }

        response = dynamodb.scan(
            TableName=collection_name,
            FilterExpression=filter_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            Limit=limit,
        )

        items = response.get("Items", [])
        documents = []

        for item in items:
            try:
                document_data = json.loads(item.get("data", {}).get("S", "{}"))
                documents.append(
                    {
                        "id": item.get("id", {}).get("S"),
                        "data": document_data,
                        "updated_at": item.get("updated_at", {}).get("N"),
                    }
                )
            except json.JSONDecodeError:
                continue

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
            "scanned_count": response.get("ScannedCount", 0),
            "last_evaluated_key": response.get("LastEvaluatedKey"),
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": e.response["Error"]["Code"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
