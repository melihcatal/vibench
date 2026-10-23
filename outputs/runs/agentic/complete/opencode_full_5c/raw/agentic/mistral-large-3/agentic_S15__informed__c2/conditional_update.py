import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Dict, Any, Optional


def get_dynamodb_table():
    """Initialize and return a DynamoDB table resource." ""
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "documents")
    return dynamodb.Table(table_name)


def conditional_update(
    document_id: str, 
    update_expression: str, 
    condition_expression: str, 
    expression_attribute_values: Dict[str, Any], 
    partition_key: str = "id"
) -> Dict[str, Any]:
    """
    Applies a conditional or version-aware update to a document in Amazon DynamoDB.
    
    Args:
        document_id: The primary identifier of the document.
        update_expression: The update expression for DynamoDB.
        condition_expression: The condition expression for the update.
        expression_attribute_values: The values for the update and condition expressions.
        partition_key: The partition key attribute name (default: "id").
        
    Returns:
        The response from DynamoDB after applying the update.
    """
    table = get_dynamodb_table()
    response = table.update_item(
        Key={partition_key: document_id},
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )
    return response