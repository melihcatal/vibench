import boto3

from document_client import load_document_client_config
from document_models import DocumentExtractionRequest


def extract_invoice_fields(document_bytes: bytes) -> dict:
    config = load_document_client_config()
    textract = boto3.client("textract", region_name=config.aws_region)
    request = DocumentExtractionRequest(document_bytes=document_bytes, scenario="invoice")
    response = textract.analyze_document(
        Document={"Bytes": request.document_bytes},
        FeatureTypes=["FORMS", "TABLES"],
    )
    fields = {"vendor": None, "date": None, "total": None, "line_items": []}
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "KEY_VALUE_SET":
            text = block.get("Text") or ""
            lower = text.lower()
            if "vendor" in lower and not fields["vendor"]:
                fields["vendor"] = text
            elif "date" in lower and not fields["date"]:
                fields["date"] = text
            elif "total" in lower and not fields["total"]:
                fields["total"] = text
    fields["raw"] = response
    return fields
