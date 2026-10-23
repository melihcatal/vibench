import os
from typing import Dict, Any
from database_client import get_dynamodb_client
from database_models import Document
import boto3.dynamodb.types as ddb_types

def conditional_update(table_name: str, document_id: str, update_expression: str, condition_expression: str, expression_attribute_values: Dict[str, Any]) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary identifier of the document to update.
        update_expression: The expression that specifies the updates to make to the item.
        condition_expression: The condition that must be satisfied for the update to proceed.
        expression_attribute_values: A map of attribute value tokens to the actual values.

    Returns:
        A dictionary containing the response from DynamoDB.
    """
    dynamodb = get_dynamodb_client()

    # Convert Python values to DynamoDB format
    marshaler = ddb_types.TypeSerializer()
    dynamodb_expression_attribute_values = {
        key: marshaler.serialize(value) for key, value in expression_attribute_values.items()
    }

    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            "document_id": {"S": document_id}
        },
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression,
        ExpressionAttributeValues=dynamodb_expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )
    return response
