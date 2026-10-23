from database_client import get_dynamodb_client
from database_models import Document
from typing import List, Any
import json

def query_documents(table_name: str, index_name: str, key_condition_expression: str, expression_attribute_values: dict) -> List[Document]:
    dynamodb = get_dynamodb_client()

    # Convert Python types to DynamoDB JSON format for expression_attribute_values
    dynamodb_expression_attribute_values = {}
    for k, v in expression_attribute_values.items():
        if isinstance(v, str):
            dynamodb_expression_attribute_values[k] = {'S': v}
        elif isinstance(v, (int, float)):
            dynamodb_expression_attribute_values[k] = {'N': str(v)}
        elif isinstance(v, bool):
            dynamodb_expression_attribute_values[k] = {'BOOL': v}
        elif isinstance(v, list):
            dynamodb_expression_attribute_values[k] = {'L': [{'S': item} for item in v]} # Assuming list of strings
        # Add other type mappings as needed

    response = dynamodb.query(
        TableName=table_name,
        IndexName=index_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=dynamodb_expression_attribute_values
    )
    
    documents = []
    for item in response.get('Items', []):
        deserialized_item = {k: list(v.values())[0] for k, v in item.items()}
        documents.append(Document.from_item(deserialized_item))
    return documents
