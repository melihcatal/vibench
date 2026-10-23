import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def conditional_update(
    collection_name, document_id, updates, condition_field=None, condition_value=None
):
    """
    Apply a conditional update to a stored document in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value
        updates: Dictionary of fields to update
        condition_field: Optional field name for condition
        condition_value: Optional expected value for condition

    Returns:
        dict: Result of the conditional update
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # First, fetch the current document
        get_response = dynamodb.get_item(
            TableName=collection_name, Key={"id": {"S": str(document_id)}}
        )

        if "Item" not in get_response:
            return {
                "success": False,
                "error": "Document not found",
                "document_id": document_id,
                "provider": "aws:dynamodb",
            }

        current_item = get_response["Item"]
        current_data = json.loads(current_item["data"]["S"])

        # Check condition if specified
        if condition_field and condition_value:
            if current_data.get(condition_field) != condition_value:
                return {
                    "success": False,
                    "error": f"Condition failed: {condition_field} != {condition_value}",
                    "document_id": document_id,
                    "provider": "aws:dynamodb",
                }

        # Apply updates
        updated_data = {**current_data, **updates}
        updated_data["_version"] = current_data.get("_version", 0) + 1

        # Prepare update expression
        update_expression = "SET #data = :data, #updated_at = :updated_at"
        expression_attribute_names = {"#data": "data", "#updated_at": "updated_at"}
        expression_attribute_values = {
            ":data": {"S": json.dumps(updated_data)},
            ":updated_at": {
                "S": str(os.environ.get("TIMESTAMP", "2025-01-01T00:00:00Z"))
            },
        }

        # Add condition expression if version check is needed
        condition_expression = None
        if "_version" in current_data:
            condition_expression = (
                "attribute_exists(#id) AND #data.#version = :current_version"
            )
            expression_attribute_names["#version"] = "_version"
            expression_attribute_values[":current_version"] = {
                "N": str(current_data["_version"])
            }

        # Perform conditional update
        update_response = dynamodb.update_item(
            TableName=collection_name,
            Key={"id": {"S": str(document_id)}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression=condition_expression,
            ReturnValues="ALL_NEW",
        )

        updated_item = update_response.get("Attributes", {})

        return {
            "success": True,
            "document_id": document_id,
            "updated_data": updated_data,
            "previous_version": current_data.get("_version", 0),
            "new_version": updated_data.get("_version", 1),
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return {
                "success": False,
                "error": "Conditional update failed: version mismatch or condition not met",
                "document_id": document_id,
                "provider": "aws:dynamodb",
            }
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
