import boto3

from document_models import field_text


def extract_receipt_fields(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    receipts = []
    for document in response["ExpenseDocuments"]:
        summary = document.get("SummaryFields", [])
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group.get("LineItems", []):
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item.get("LineItemExpenseFields", [])}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        receipts.append({
            "merchant": field_text(summary, "VENDOR_NAME"),
            "tax": field_text(summary, "TAX"),
            "total": field_text(summary, "TOTAL"),
            "items": items,
        })
    return {"receipts": receipts}
