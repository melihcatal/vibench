import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def conditional_update(table_name, document_id, update_data, condition_expression=None):
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.

    Args:
        table_name: Name of the DynamoDB table
        document_id: Primary key identifier for the document
        update_data: New data to update
        condition_expression: Optional condition expression for conditional update

    Returns:
        dict: Response from DynamoDB operation
    """
    dynamodb = client(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    update_params = {
        "TableName": table_name,
        "Key": {"document_id": {"S": document_id}},
        "UpdateExpression": "SET #data = :data, #updated_at = :updated_at",
        "ExpressionAttributeNames": {"#data": "data", "#updated_at": "updated_at"},
        "ExpressionAttributeValues": {
            ":data": {"S": json.dumps(update_data)},
            ":updated_at": {
                "S": str(os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"))
            },
        },
        "ReturnValues": "ALL_NEW",
    }

    if condition_expression:
        update_params["ConditionExpression"] = condition_expression

    try:
        response = dynamodb.update_item(**update_params)
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise Exception(
                "Condition check failed: document does not meet update conditions"
            )
        raise Exception(
            f"DynamoDB conditional update failed: {e.response['Error']['Message']}"
        )
