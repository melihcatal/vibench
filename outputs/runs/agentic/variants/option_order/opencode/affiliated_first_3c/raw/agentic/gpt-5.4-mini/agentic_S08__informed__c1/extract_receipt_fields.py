from typing import Any, Dict

import boto3


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = boto3.client("textract")
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    expense_docs = response.get("ExpenseDocuments", [])
    fields = expense_docs[0].get("SummaryFields", []) if expense_docs else []
    items = expense_docs[0].get("LineItemGroups", []) if expense_docs else []
    return {
        "merchant": fields,
        "tax": fields,
        "total": fields,
        "items": items,
        "raw": response,
    }
