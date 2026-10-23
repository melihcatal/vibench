import os
import boto3
from typing import Optional
from document_models import NormalizedExpense


def expense_record_store(
    expense: NormalizedExpense, record_id: Optional[str] = None
) -> None:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    table = dynamodb.Table("ExpenseRecords")
    item = expense.model_dump()
    item["record_type"] = "normalized_expense"
    if record_id:
        item["id"] = record_id
    table.put_item(Item=item)
