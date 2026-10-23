import os
from typing import Any, Dict
import boto3
from document_client import get_document_payload, normalize_text
from document_models import build_invoice_result


def extract_invoice_fields(source: Any) -> Dict[str, Any]:
    payload = get_document_payload(source)
    client = boto3.client('textract', region_name=os.getenv('AWS_REGION'))
    response = client.analyze_expense(Document={'Bytes': payload})
    return build_invoice_result(response, normalize_text)
