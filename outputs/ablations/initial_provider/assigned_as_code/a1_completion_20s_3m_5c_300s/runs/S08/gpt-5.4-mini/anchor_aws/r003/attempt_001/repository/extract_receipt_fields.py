from document_client import build_textract_client, document_bytes, normalize_text


def extract_receipt_fields(payload, config=None):
    client = build_textract_client(config)
    response = client.analyze_expense(Document={"Bytes": document_bytes(payload)})
    receipts = []
    for document in response.get("ExpenseDocuments", []):
        fields = {f["Type"]["Text"]: normalize_text(f["ValueDetection"].get("Text", "")) for f in document.get("SummaryFields", [])}
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group.get("LineItems", []):
                values = {f["Type"]["Text"]: normalize_text(f["ValueDetection"].get("Text", "")) for f in item.get("LineItemExpenseFields", [])}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        receipts.append({"merchant": fields.get("VENDOR_NAME"), "tax": fields.get("TAX"), "total": fields.get("TOTAL"), "items": items})
    return {"receipts": receipts}
