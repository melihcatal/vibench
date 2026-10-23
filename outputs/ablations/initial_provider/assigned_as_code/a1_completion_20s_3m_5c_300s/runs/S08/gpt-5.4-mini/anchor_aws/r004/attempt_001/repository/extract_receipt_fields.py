from document_client import textract_client


def extract_receipt_fields(payload, config=None):
    client = textract_client(config)
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    receipts = []
    for document in response.get("ExpenseDocuments", []):
        fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document.get("SummaryFields", [])}
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group.get("LineItems", []):
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item.get("LineItemExpenseFields", [])}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        receipts.append({"merchant": fields.get("VENDOR_NAME") or fields.get("RECEIVER_NAME"), "tax": fields.get("TOTAL_TAX") or fields.get("TAX"), "total": fields.get("TOTAL"), "items": items})
    return {"receipts": receipts}
