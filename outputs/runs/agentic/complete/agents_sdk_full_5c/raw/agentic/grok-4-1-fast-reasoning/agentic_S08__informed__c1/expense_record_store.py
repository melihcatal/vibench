import boto3
import os
import uuid
from typing import Dict, Any
from document_models import NormalizedExpense

def store_expense_record(expense: NormalizedExpense) -> str:
    expense_id = expense.get('id', str(uuid.uuid4()))
    expense_record = expense.copy()
    expense_record['id'] = expense_id
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    table = dynamodb.Table(os.getenv('EXPENSE_TABLE_NAME', 'Expenses'))
    table.put_item(Item=expense_record)
    return expense_id
