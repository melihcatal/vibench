import boto3


def extract_invoice_fields(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    invoices = []
    for document in response["ExpenseDocuments"]:
        fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document["SummaryFields"]}
        items = []
        for group in document.get("LineItemGroups", []):
            for item in group["LineItems"]:
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item["LineItemExpenseFields"]}
                items.append({"description": values.get("ITEM"), "quantity": values.get("QUANTITY"), "amount": values.get("PRICE")})
        invoices.append({"vendor": fields.get("VENDOR_NAME"), "date": fields.get("INVOICE_RECEIPT_DATE"),
                         "total": fields.get("TOTAL"), "line_items": items})
    return {"invoices": invoices}
