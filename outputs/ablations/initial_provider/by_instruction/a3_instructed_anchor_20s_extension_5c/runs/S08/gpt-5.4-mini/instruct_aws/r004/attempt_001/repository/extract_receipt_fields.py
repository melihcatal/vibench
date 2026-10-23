from typing import Any, Dict

from document_client import create_textract_client, load_document_config


def extract_receipt_fields(document_uri: str = None, document_bytes: bytes = None) -> Dict[str, Any]:
    client = create_textract_client()
    cfg = load_document_config()
    if document_bytes is not None:
        response = client.analyze_expense(Document={"Bytes": document_bytes})
    else:
        response = client.analyze_expense(
            Document={"S3Object": {"Bucket": cfg["s3_bucket"], "Name": document_uri}}
        )
    return {"provider": "aws_textract", "document_uri": document_uri, "response": response}
