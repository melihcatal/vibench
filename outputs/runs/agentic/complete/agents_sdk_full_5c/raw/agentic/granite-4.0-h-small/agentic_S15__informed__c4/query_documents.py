import os
from database_client import get_dynamodb_client
from database_models import query_item_payload

def query_documents(partition_key: str, filter_expression: str = None, expression_attribute_values: dict = None):
    """Query documents by partition key.
    Optional filter expression and attribute values can be supplied.
    Returns a list of item dicts.
    """
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    payload = query_item_payload(partition_key, filter_expression, expression_attribute_values)
    response = client.query(**payload)
    return response.get('Items', [])
