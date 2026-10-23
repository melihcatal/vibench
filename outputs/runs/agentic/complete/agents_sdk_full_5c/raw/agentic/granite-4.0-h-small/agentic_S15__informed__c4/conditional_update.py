import os
from database_client import get_dynamodb_client
from database_models import conditional_update_payload

def conditional_update(identifier: str, update_expression: str, expression_attribute_values: dict):
    """Apply a conditional / version-aware update to a DynamoDB document.
    Uses a provided UpdateExpression and Values dict; the SDK ensures the condition
    (e.g., version attribute) is met before applying.
    """
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    payload = conditional_update_payload(identifier, update_expression, expression_attribute_values)
    response = client.update_item(**payload)
    print('Conditional update response:', response)
