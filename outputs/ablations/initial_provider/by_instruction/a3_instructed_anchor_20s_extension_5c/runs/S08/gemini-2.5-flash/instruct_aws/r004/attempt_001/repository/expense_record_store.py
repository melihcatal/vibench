import boto3
from typing import Dict, Any
from document_models import NormalizedExpense
import json

# Replace with your DynamoDB table name
TABLE_NAME = 'ExpenseRecords'

def store_expense_record(normalized_expense: NormalizedExpense) -> Dict[str, Any]:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    # DynamoDB requires clean JSON-serializable types
    # Convert dataclass to dict and then serialize to JSON string for complex objects
    item = {
        'record_id': str(hash(json.dumps(normalized_expense.raw_extraction_data, sort_keys=True))), # Unique ID for the record
        'document_type': normalized_expense.document_type,
        'vendor_name': normalized_expense.vendor_name,
        'transaction_date': normalized_expense.transaction_date,
        'total_amount': normalized_expense.total_amount,
        'currency': normalized_expense.currency,
        'line_items': json.dumps(normalized_expense.line_items), # Store list of dicts as JSON string
        'raw_extraction_data': json.dumps(normalized_expense.raw_extraction_data) # Store raw data as JSON string
    }

    try:
        response = table.put_item(Item=item)
        return {
            'status': 'success',
            'message': 'Expense record stored successfully.',
            'dynamodb_response': response
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to store expense record: {e}',
            'error_details': str(e)
        }
