import boto3
from document_client import get_aws_dynamodb_config
from document_models import NormalizedExpense
import json
import uuid

def persist_expense_record(expense_record: NormalizedExpense, table_name: str = 'ExpenseRecords') -> dict:
    config = get_aws_dynamodb_config()
    region_name = config.get('region_name')
    aws_access_key_id = config.get('aws_access_key_id')
    aws_secret_access_key = config.get('aws_secret_access_key')

    if not all([region_name, aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS credentials (region, access key, secret key) must be configured for DynamoDB.")

    dynamodb = boto3.resource(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    table = dynamodb.Table(table_name)

    # Generate a unique ID for the expense record
    record_id = str(uuid.uuid4())
    
    # Convert NormalizedExpense dataclass to a dictionary suitable for DynamoDB
    # DynamoDB doesn't directly support nested lists of dicts if they contain mixed types or empty strings
    # It's better to convert dataclass to dict and handle potential issues
    item = {
        'record_id': record_id,
        'document_type': expense_record.document_type,
        'vendor_name': expense_record.vendor_name,
        'transaction_date': expense_record.transaction_date,
        'total_amount': float(expense_record.total_amount) if expense_record.total_amount is not None else None,
        'currency': expense_record.currency,
        'line_items': json.loads(json.dumps(expense_record.line_items)), # Ensure JSON serializable
        'raw_extraction_data': json.loads(json.dumps(expense_record.raw_extraction_data)) # Ensure JSON serializable
    }
    
    # Remove None values as DynamoDB doesn't store them
    item = {k: v for k, v in item.items() if v is not None}

    try:
        response = table.put_item(Item=item)
        return {
            "status": "success",
            "record_id": record_id,
            "dynamodb_response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to persist expense record to DynamoDB: {e}"
        }
