import os
from boto3 import client
from botocore.exceptions import ClientError
import json


def conditional_update(
    collection_name, document_id, updates, condition_expression=None
):
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.

    Args:
        collection_name: The DynamoDB table name
        document_id: The primary key value for the document
        updates: Dictionary of fields to update
        condition_expression: Optional condition expression for conditional update

    Returns:
        dict: Update response or error information
    """
    try:
        # Initialize DynamoDB client with AWS credentials
        dynamodb = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # First, fetch the current document to merge updates
        get_response = dynamodb.get_item(
            TableName=collection_name, Key={"id": {"S": document_id}}
        )

        current_item = get_response.get("Item")
        if not current_item:
            return {
                "success": False,
                "error": "Document not found",
                "document_id": document_id,
            }

        # Parse current data
        current_data = json.loads(current_item.get("data", {}).get("S", "{}"))

        # Merge updates
        updated_data = {**current_data, **updates}

        # Prepare update expression
        update_expression = "SET #data = :data, #updated_at = :updated_at"
        expression_attribute_names = {"#data": "data", "#updated_at": "updated_at"}
        expression_attribute_values = {
            ":data": {"S": json.dumps(updated_data)},
            ":updated_at": {"N": str(int(os.time()))},
        }

        # Add condition expression if provided
        update_kwargs = {
            "TableName": collection_name,
            "Key": {"id": {"S": document_id}},
            "UpdateExpression": update_expression,
            "ExpressionAttributeNames": expression_attribute_names,
            "ExpressionAttributeValues": expression_attribute_values,
            "ReturnValues": "ALL_NEW",
        }

        if condition_expression:
            update_kwargs["ConditionExpression"] = condition_expression

        # Perform the update
        response = dynamodb.update_item(**update_kwargs)

        return {
            "success": True,
            "document_id": document_id,
            "updated_data": updated_data,
            "attributes": response.get("Attributes"),
            "response_metadata": response.get("ResponseMetadata"),
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return {
                "success": False,
                "error": "Condition check failed",
                "error_code": error_code,
                "document_id": document_id,
            }
        return {"success": False, "error": str(e), "error_code": error_code}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON in stored document: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
