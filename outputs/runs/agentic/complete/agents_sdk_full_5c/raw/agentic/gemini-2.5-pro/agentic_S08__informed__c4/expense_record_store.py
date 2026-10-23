import os
import boto3
from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError
from document_models import NormalizedExpense
import json
from decimal import Decimal

# Helper to convert floats to Decimals for DynamoDB
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            return Decimal(str(obj))
        return super(JSONEncoder, self).default(obj)

def persist_expense_record(expense: NormalizedExpense):
    """
    Persists a normalized expense record into an Amazon DynamoDB table.

    The table name is read from the DYNAMODB_TABLE_NAME environment variable.
    """
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")

    try:
        # Using low-level client for better control over serialization
        dynamodb_client = boto3.client("dynamodb")
        
        # Convert Pydantic model to dict, then to DynamoDB JSON format
        # This handles nested structures and types like float -> Decimal
        item_dict = json.loads(expense.model_dump_json(), parse_float=Decimal)
        
        # Serialize Python dict to DynamoDB item format
        serializer = TypeSerializer()
        dynamodb_item = {k: serializer.serialize(v) for k, v in item_dict.items()}

        dynamodb_client.put_item(
            TableName=table_name,
            Item=dynamodb_item
        )
        print(f"Successfully saved expense {expense.expense_id} to DynamoDB.")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"Failed to save to DynamoDB. Error: {error_code}")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e

