import os
from typing import Dict, Any
from document_client import get_dynamodb_client
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense, table_name: str) -> Dict[str, Any]:
    """
    Persists normalized expense records in an AWS DynamoDB managed document store.
    """
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table(table_name)

    try:
        if 'id' not in expense_record or not expense_record['id']:
            raise ValueError("Expense record must have a unique 'id' for DynamoDB.")

        response = table.put_item(
            Item=expense_record
        )
        return response
    except Exception as e:
        print(f"Error persisting expense record to DynamoDB: {e}")
        raise
