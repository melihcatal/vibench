import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def query_documents(collection_name, field_name, field_value, limit=100):
    """
    Query documents by a field value from DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        field_name: The field name to query on
        field_value: The field value to match
        limit: Maximum number of documents to return

    Returns:
        list: Matching documents
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
        # This example uses a scan with filter expression (not efficient for large tables)
        # In production, you would use a GSI on the field you want to query

        # Build filter expression
        filter_expression = f"contains(#data, :value)"

        response = dynamodb.scan(
            TableName=collection_name,
            FilterExpression=filter_expression,
            ExpressionAttributeNames={"#data": "data"},
            ExpressionAttributeValues={
                ":value": {"S": f'"{field_name}":"{field_value}"'}
            },
            Limit=limit,
        )

        documents = []
        for item in response.get("Items", []):
            try:
                document_data = json.loads(item["data"]["S"])
                documents.append(
                    {
                        "id": item["id"]["S"],
                        "data": document_data,
                        "updated_at": item.get("updated_at", {}).get("S"),
                    }
                )
            except json.JSONDecodeError:
                continue

        # Handle pagination
        while "LastEvaluatedKey" in response and len(documents) < limit:
            response = dynamodb.scan(
                TableName=collection_name,
                FilterExpression=filter_expression,
                ExpressionAttributeNames={"#data": "data"},
                ExpressionAttributeValues={
                    ":value": {"S": f'"{field_name}":"{field_value}"'}
                },
                ExclusiveStartKey=response["LastEvaluatedKey"],
                Limit=limit - len(documents),
            )

            for item in response.get("Items", []):
                try:
                    document_data = json.loads(item["data"]["S"])
                    documents.append(
                        {
                            "id": item["id"]["S"],
                            "data": document_data,
                            "updated_at": item.get("updated_at", {}).get("S"),
                        }
                    )
                except json.JSONDecodeError:
                    continue

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
            "field_name": field_name,
            "field_value": field_value,
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "field_name": field_name,
            "field_value": field_value,
            "provider": "aws:dynamodb",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "field_name": field_name,
            "field_value": field_value,
            "provider": "aws:dynamodb",
        }
