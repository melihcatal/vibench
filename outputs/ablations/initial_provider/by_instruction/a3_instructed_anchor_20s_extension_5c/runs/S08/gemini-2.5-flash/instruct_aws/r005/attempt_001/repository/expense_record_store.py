from document_client import get_dynamodb_client
from document_models import ExtractedExpense
import json
import os
import uuid

def persist_expense_record(expense: ExtractedExpense) -> dict:
    """
    Persists normalized expense records in AWS DynamoDB.

    Args:
        expense: The ExtractedExpense object to persist.

    Returns:
        A dictionary containing the response from DynamoDB put_item operation.
    """
    dynamodb_client = get_dynamodb_client()
    table_name = os.environ.get("DYNAMODB_EXPENSE_TABLE_NAME", "ExpenseRecords")

    item_id = str(uuid.uuid4())

    # Convert ExtractedExpense to a dictionary for DynamoDB
    expense_dict = expense.dict()
    # DynamoDB requires non-empty strings and handles various types. Lists/dicts need to be handled.
    # For simplicity, we'll convert the entire object to a JSON string for complex fields
    # or ensure basic types are correctly mapped.

    # Clean up None values and convert complex types to string if necessary for simple mapping
    cleaned_item = {
        "id": {"S": item_id},
        "vendor_name": {"S": expense.vendor_name} if expense.vendor_name else {"NULL": True},
        "merchant_name": {"S": expense.merchant_name} if expense.merchant_name else {"NULL": True},
        "document_date": {"S": expense.document_date} if expense.document_date else {"NULL": True},
        "tax_amount": {"S": expense.tax_amount} if expense.tax_amount else {"NULL": True},
        "total_amount": {"S": expense.total_amount} if expense.total_amount else {"NULL": True},
        "currency": {"S": expense.currency} if expense.currency else {"NULL": True},
        "line_items": {"S": json.dumps([item.dict() for item in expense.line_items])} if expense.line_items else {"NULL": True},
        "additional_data": {"S": json.dumps(expense.additional_data)} if expense.additional_data else {"NULL": True},
    }

    # Remove keys with {"NULL": True} if they are not needed or if all values are None
    item_attributes = {k: v for k, v in cleaned_item.items() if not (isinstance(v, dict) and "NULL" in v and v["NULL"] is True)}

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item_attributes
    )

    return response
