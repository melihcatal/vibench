import boto3

from document_client import textract_client


def extract_invoice_fields(document_bytes: bytes) -> dict:
    client = textract_client()
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    summary = {"vendor": None, "date": None, "total": None, "line_items": []}
    for expense in response.get("ExpenseDocuments", []):
        for field in expense.get("SummaryFields", []):
            t = field.get("Type", {}).get("Text")
            v = field.get("ValueDetection", {}).get("Text")
            if t == "VENDOR_NAME":
                summary["vendor"] = v
            elif t == "INVOICE_RECEIPT_DATE":
                summary["date"] = v
            elif t in {"TOTAL", "AMOUNT_DUE"}:
                summary["total"] = v
        for group in expense.get("LineItemGroups", []):
            for item in group.get("LineItems", []):
                line = {}
                for field in item.get("LineItemExpenseFields", []):
                    t = field.get("Type", {}).get("Text")
                    v = field.get("ValueDetection", {}).get("Text")
                    if t:
                        line[t.lower()] = v
                if line:
                    summary["line_items"].append(line)
    return summary
