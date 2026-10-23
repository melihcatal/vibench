import os
from typing import Dict, Any
from document_client import get_aws_dynamodb_client
from document_models import NormalizedExpense
import uuid
import json
from decimal import Decimal

# Helper to convert float to Decimal for DynamoDB
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

def persist_expense_record(expense_record: NormalizedExpense, table_name: str) -> Dict[str, Any]:
    """Persists normalized expense records in an AWS DynamoDB table.

    Args:
        expense_record: A NormalizedExpense object to persist.
        table_name: The name of the DynamoDB table.

    Returns:
        A dictionary containing the response from DynamoDB put_item operation.
    """
    dynamodb_client = get_aws_dynamodb_client()

    # Convert NormalizedExpense object to a dictionary for DynamoDB
    # DynamoDB doesn't directly support floats in all contexts for numbers,
    # so converting to Decimal where necessary or ensuring JSON string for complex objects.
    item = expense_record.__dict__

    # Convert float values to Decimal for DynamoDB numbers
    for key, value in item.items():
        if isinstance(value, float):
            item[key] = Decimal(str(value)) # Convert to string first to avoid precision issues
        elif isinstance(value, list) and all(isinstance(i, dict) for i in value): # for line_items
            # Convert line_items to JSON string to store as a single attribute if needed, or handle complex structure
            # For simplicity, converting to JSON string. A more advanced design might use nested maps/lists if supported.
            item[key] = json.dumps(value, cls=CustomJsonEncoder)
        elif isinstance(value, dict):
            item[key] = json.dumps(value, cls=CustomJsonEncoder)

    # Add a unique ID for the item if it doesn't have one
    if 'id' not in item or not item['id']:
        item['id'] = str(uuid.uuid4())
    
    # For the `document_type` attribute, if it's not present, add a default or raise an error
    if 'document_type' not in item or not item['document_type']:
        raise ValueError("document_type is a required field for expense records.")

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={
            key: {'S': str(value)} if isinstance(value, str) else
                 {'N': str(value)} if isinstance(value, (int, Decimal)) else
                 {'BOOL': bool(value)} if isinstance(value, bool) else
                 {'L': [{'S': i} for i in value]} if isinstance(value, list) and all(isinstance(i, str) for i in value) else
                 {'M': {k: {'S': str(v)} for k, v in value.items()}} if isinstance(value, dict) else
                 {'NULL': True} if value is None else
                 # Fallback for other types, might need more specific handling
                 {'S': json.dumps(value, cls=CustomJsonEncoder)}
            for key, value in item.items()
        }
    )

    return response
