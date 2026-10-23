import os
import boto3
from typing import Dict, Any
from document_client import DocumentAIClient
from document_models import NormalizedExpense
import json

def persist_expense_record(expense_record: NormalizedExpense, table_name: str = "ExpenseRecords") -> Dict[str, Any]:
    dynamodb_client = DocumentAIClient().get_dynamodb_client()

    # DynamoDB requires specific types and does not accept empty strings or lists directly for all operations.
    # We'll convert the NormalizedExpense to a dictionary, then filter out None values for basic types.
    item = expense_record.to_dict()

    # Convert float to Decimal for DynamoDB (boto3 handles this automatically if `decimal` is available, but explicit conversion can prevent issues)
    # For this example, we'll keep it simple and assume default boto3 behavior or handle client-side conversion if needed for more complex types.
    # Boto3's put_item automatically handles Python types to DynamoDB types for basic scalars and lists of scalars.
    # Nested dicts and lists of dicts need careful handling if they contain empty strings/None.

    # Simple serialization for DynamoDB. For complex types or if specific attributes must be present, more robust handling is needed.
    # For now, let's convert the entire object to a JSON string if it contains complex nested structures for raw_data or line_items
    # Or, ensure each field is directly compatible. Let's aim for direct compatibility by cleaning None values.
    cleaned_item = {
        k: v for k, v in item.items() if v is not None and v != []
    }

    # DynamoDB primary key for a simple table
    # Assuming a 'record_id' for simplicity. In a real app, this would be generated or provided.
    if "record_id" not in cleaned_item:
        import uuid
        cleaned_item["record_id"] = str(uuid.uuid4())

    try:
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item={
                key: {'S': str(value)} if isinstance(value, str) else 
                     {'N': str(value)} if isinstance(value, (int, float)) else 
                     {'BOOL': value} if isinstance(value, bool) else 
                     {'L': [{'S': str(i)} for i in value]} if isinstance(value, list) and all(isinstance(i, (str, int, float, bool)) for i in value) else 
                     {'M': {inner_k: {'S': str(inner_v)} if isinstance(inner_v, str) else 
                               {'N': str(inner_v)} if isinstance(inner_v, (int, float)) else 
                               {'BOOL': inner_v} if isinstance(inner_v, bool) else 
                               {} # Fallback for unsupported inner types
                               for inner_k, inner_v in value.items()}} if isinstance(value, dict) else
                     {}
                for key, value in cleaned_item.items()
            }
        )
        return {"success": True, "response": response, "record_id": cleaned_item["record_id"]}
    except Exception as e:
        return {"success": False, "error": str(e)}
