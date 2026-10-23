import os
from typing import Any, Dict

from document_client import create_textract_client, load_document_config
from document_models import DocumentRequest


def extract_invoice_fields(document_uri: str = None, document_bytes: bytes = None) -> Dict[str, Any]:
    client = create_textract_client()
    cfg = load_document_config()
    request = DocumentRequest(document_uri=document_uri, document_bytes=document_bytes, fields=["vendor", "date", "total", "line_items"])
    if request.document_bytes is not None:
        response = client.analyze_document(
            Document={"Bytes": request.document_bytes},
            FeatureTypes=["TABLES", "FORMS"],
        )
    else:
        response = client.analyze_document(
            Document={"S3Object": {"Bucket": cfg["s3_bucket"], "Name": request.document_uri}},
            FeatureTypes=["TABLES", "FORMS"],
        )
    return {
        "provider": "aws_textract",
        "requested_fields": request.fields,
        "document_uri": request.document_uri,
        "response": response,
    }
