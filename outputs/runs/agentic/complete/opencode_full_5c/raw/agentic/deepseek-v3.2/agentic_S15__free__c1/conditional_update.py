import os
from boto3 import client
from botocore.exceptions import ClientError
import json
import time


def conditional_update(
    collection_name, document_id, updates, condition_field=None, condition_value=None
):
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key identifier
        updates: Dictionary of fields to update
        condition_field: Optional field to check in condition
        condition_value: Expected value for condition field

    Returns:
        dict: Update result with status
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # First, fetch the current document to apply updates
        get_response = dynamodb.get_item(
            TableName=collection_name, Key={"id": {"S": document_id}}
        )

        if "Item" not in get_response:
            return {
                "success": False,
                "error": "Document not found for conditional update",
                "document_id": document_id,
                "provider": "aws:dynamodb",
            }

        current_item = get_response["Item"]
        current_data = (
            json.loads(current_item["data"]["S"]) if "data" in current_item else {}
        )

        # Check condition if specified
        if condition_field and condition_value:
            if condition_field not in current_data:
                return {
                    "success": False,
                    "error": f"Condition field {condition_field} not found in document",
                    "document_id": document_id,
                    "provider": "aws:dynamodb",
                }

            if str(current_data[condition_field]) != str(condition_value):
                return {
                    "success": False,
                    "error": f"Condition not met: {condition_field}={current_data[condition_field]} != {condition_value}",
                    "document_id": document_id,
                    "provider": "aws:dynamodb",
                }

        # Apply updates to current data
        updated_data = current_data.copy()
        updated_data.update(updates)
        updated_data["_version"] = updated_data.get("_version", 0) + 1
        updated_data["_updated_at"] = time.time()

        # Prepare update expression for DynamoDB
        update_expression = "SET #data = :new_data, #updated_at = :timestamp"
        expression_attribute_names = {"#data": "data", "#updated_at": "updated_at"}
        expression_attribute_values = {
            ":new_data": {"S": json.dumps(updated_data)},
            ":timestamp": {"S": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
        }

        # Add condition expression if provided
        condition_expression = None
        if condition_field and condition_value:
            # For DynamoDB conditional update, we need to check the JSON string
            condition_expression = "contains(#data, :condition_check)"
            expression_attribute_names["#data"] = "data"
            expression_attribute_values[":condition_check"] = {
                "S": f'"{condition_field}":"{condition_value}"'
            }

        # Perform conditional update
        update_response = dynamodb.update_item(
            TableName=collection_name,
            Key={"id": {"S": document_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression=condition_expression,
            ReturnValues="ALL_NEW",
        )

        # Parse the updated item
        updated_item = update_response.get("Attributes", {})

        return {
            "success": True,
            "document_id": document_id,
            "updated_fields": list(updates.keys()),
            "new_version": updated_data.get("_version"),
            "condition_checked": condition_field is not None,
            "provider": "aws:dynamodb",
            "table": collection_name,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "ConditionalCheckFailedException":
            return {
                "success": False,
                "error": "Conditional update failed: condition not met",
                "document_id": document_id,
                "provider": "aws:dynamodb",
            }
        return {
            "success": False,
            "error": str(e),
            "document_id": document_id,
            "provider": "aws:dynamodb",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "document_id": document_id,
            "provider": "aws:dynamodb",
        }
