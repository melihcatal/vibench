import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def query_documents(table_name, field_name, field_value, index_name=None):
    """
    Queries documents by a field value or partition-style key in DynamoDB.

    Args:
        table_name: Name of the DynamoDB table
        field_name: Name of the field to query
        field_value: Value to match
        index_name: Optional Global Secondary Index name

    Returns:
        list: List of matching documents
    """
    dynamodb = client(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    query_params = {
        "TableName": table_name,
        "KeyConditionExpression": f"{field_name} = :val",
        "ExpressionAttributeValues": {":val": {"S": field_value}},
    }

    if index_name:
        query_params["IndexName"] = index_name

    try:
        response = dynamodb.query(**query_params)
        documents = []

        for item in response.get("Items", []):
            if "data" in item:
                documents.append(json.loads(item["data"]["S"]))

        return documents
    except ClientError as e:
        raise Exception(f"DynamoDB query failed: {e.response['Error']['Message']}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse document data: {str(e)}")
