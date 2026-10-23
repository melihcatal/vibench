import boto3

from document_client import require_env
from document_models import StructuredDocumentResponse, normalize_money


def extract_receipt_fields(document_bytes: bytes) -> dict:
    client = boto3.client(
        "textract",
        aws_access_key_id=require_env("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=require_env("AWS_SECRET_ACCESS_KEY"),
    )
    result = client.analyze_expense(Document={"Bytes": document_bytes})
    doc = result["ExpenseDocuments"][0] if result.get("ExpenseDocuments") else {}
    summary = {
        item["Type"]["Text"]: item.get("ValueDetection", {}).get("Text")
        for item in doc.get("SummaryFields", [])
    }
    items = []
    for group in doc.get("LineItemGroups", []):
        for line in group.get("LineItems", []):
            items.append(
                {
                    k: v.get("Text")
                    for k, v in line.get("LineItemExpenseFields", {}).items()
                    if v
                }
            )
    response = StructuredDocumentResponse(
        document_type="receipt",
        fields={
            "merchant": summary.get("VENDOR_NAME"),
            "tax": normalize_money(summary.get("TOTAL_TAX")),
            "total": normalize_money(summary.get("TOTAL")),
            "items": items,
        },
        raw={"service": "boto3-textract-analyzeexpense"},
    )
    return response.__dict__
