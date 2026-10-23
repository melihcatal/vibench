import os
from typing import List, Dict, Any
from database_client import get_dynamodb_client
from database_models import Document
import boto3.dynamodb.types as ddb_types

def query_documents(table_name: str, index_name: str, key_condition_expression: str, expression_attribute_values: Dict[str, Any]) -> List[Document]:
    """
    Queries documents from an AWS DynamoDB table by a field value or partition-style key.

    Args:
        table_name: The name of the DynamoDB table.
        index_name: The name of the GSI or LSI to query.
        key_condition_expression: The condition that specifies the key values for items to be retrieved.
        expression_attribute_values: A map of attribute value tokens to the actual values.

    Returns:
        A list of matching Document objects.
    """
    dynamodb = get_dynamodb_client()

    # Convert Python values to DynamoDB format
    marshaler = ddb_types.TypeSerializer()
    dynamodb_expression_attribute_values = {
        key: marshaler.serialize(value) for key, value in expression_attribute_values.items()
    }

    response = dynamodb.query(
        TableName=table_name,
        IndexName=index_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=dynamodb_expression_attribute_values
    )

    documents = []
    for item in response.get("Items", []):
        documents.append(Document.from_item(item))
    return documents
