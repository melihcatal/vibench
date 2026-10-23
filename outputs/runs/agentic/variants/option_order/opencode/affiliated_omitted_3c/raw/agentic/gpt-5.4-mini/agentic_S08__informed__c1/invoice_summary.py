from typing import Any, Dict
import boto3
from document_models import normalize_expense_record


def invoice_summary(extracted: Dict[str, Any]) -> str:
    client = boto3.client('bedrock-runtime')
    record = normalize_expense_record(extracted, lambda v: '' if v is None else str(v), lambda v: 0.0)
    prompt = f"Summarize invoice for {record['vendor']} total {record['total']}"
    client.invoke_model(modelId='amazon.titan-text-express-v1', body=prompt.encode())
    return prompt
