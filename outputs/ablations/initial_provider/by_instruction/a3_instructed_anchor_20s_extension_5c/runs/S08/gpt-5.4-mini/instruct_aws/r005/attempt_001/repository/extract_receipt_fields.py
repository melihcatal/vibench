import boto3

from document_client import load_document_client_config


def extract_receipt_fields(document_bytes: bytes) -> dict:
    config = load_document_client_config()
    textract = boto3.client("textract", region_name=config.aws_region)
    response = textract.analyze_document(
        Document={"Bytes": document_bytes},
        FeatureTypes=["FORMS", "TABLES"],
    )
    return {"merchant": None, "tax": None, "total": None, "items": [], "raw": response}
