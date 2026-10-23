import os
from typing import Any, Dict

import boto3

from document_client import parse_textract_response, textract_client


def extract_invoice_fields(document_bytes: bytes = None, document_uri: str = None) -> Dict[str, Any]:
    client = textract_client()
    if document_bytes is not None:
        response = client.analyze_document(
            Document={"Bytes": document_bytes},
            FeatureTypes=["FORMS", "TABLES"],
        )
    else:
        response = client.analyze_document(
            Document={"S3Object": {"Bucket": os.environ["AWS_S3_BUCKET"], "Name": document_uri}},
            FeatureTypes=["FORMS", "TABLES"],
        )
    parsed = parse_textract_response(response)
    invoice = {
        "vendor": parsed.fields.get("vendor", parsed.fields.get("merchant_name")),
        "date": parsed.fields.get("date", parsed.fields.get("invoice_date")),
        "total": parsed.fields.get("total", parsed.fields.get("amount_due")),
        "line_items": parsed.fields.get("line_items", []),
        "provider": parsed.provider,
    }
    return invoice
