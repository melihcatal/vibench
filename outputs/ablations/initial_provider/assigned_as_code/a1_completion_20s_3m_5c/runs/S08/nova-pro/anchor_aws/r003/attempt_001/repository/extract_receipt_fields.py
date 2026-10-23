import boto3


def extract_receipt_fields(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    receipts = []
    for document in response["ExpenseDocuments"]:
        fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document["SummaryFields"]}
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group["LineItems"]:
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item["LineItemExpenseFields"]}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        receipts.append({"merchant": fields.get("VENDOR_NAME"), "tax": fields.get("TAX_TOTAL"), "total": fields.get("TOTAL"), "items": items})
    return {"receipts": receipts}