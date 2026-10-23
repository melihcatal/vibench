import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def query_documents(collection_name, field_name, field_value, limit=100):
    """
    Queries documents by a field value from DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        field_name: The field to query on
        field_value: The value to match
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

        # For DynamoDB, we need to use a GSI or scan for field queries
        # This implementation uses a scan for simplicity (not production-optimal)

        # Build filter expression
        filter_expression = f"contains(#data, :field_value)"

        response = dynamodb.scan(
            TableName=collection_name,
            FilterExpression=filter_expression,
            ExpressionAttributeNames={"#data": "data"},
            ExpressionAttributeValues={
                ":field_value": {"S": f'"{field_name}":"{field_value}"'}
            },
            Limit=limit,
        )

        documents = []

        # Process items
        for item in response.get("Items", []):
            try:
                document_data = json.loads(item["data"]["S"]) if "data" in item else {}

                # Verify the field actually matches (scan filter is approximate)
                if field_name in document_data and str(
                    document_data[field_name]
                ) == str(field_value):
                    documents.append(
                        {
                            "id": item["id"]["S"],
                            "data": document_data,
                            "updated_at": item.get("updated_at", {}).get("S", ""),
                        }
                    )
            except (json.JSONDecodeError, KeyError):
                continue

        # Handle pagination if needed
        while "LastEvaluatedKey" in response and len(documents) < limit:
            response = dynamodb.scan(
                TableName=collection_name,
                FilterExpression=filter_expression,
                ExpressionAttributeNames={"#data": "data"},
                ExpressionAttributeValues={
                    ":field_value": {"S": f'"{field_name}":"{field_value}"'}
                },
                ExclusiveStartKey=response["LastEvaluatedKey"],
                Limit=limit - len(documents),
            )

            for item in response.get("Items", []):
                try:
                    document_data = (
                        json.loads(item["data"]["S"]) if "data" in item else {}
                    )

                    if field_name in document_data and str(
                        document_data[field_name]
                    ) == str(field_value):
                        documents.append(
                            {
                                "id": item["id"]["S"],
                                "data": document_data,
                                "updated_at": item.get("updated_at", {}).get("S", ""),
                            }
                        )
                except (json.JSONDecodeError, KeyError):
                    continue

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
            "query": {"field": field_name, "value": field_value},
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "documents": [],
            "count": 0,
            "provider": "aws:dynamodb",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "documents": [],
            "count": 0,
            "provider": "aws:dynamodb",
        }
