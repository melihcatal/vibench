import boto3
from typing import Dict, Any, List
from document_models import DocumentExtractionRequest, ReceiptFields, LineItem
from document_client import get_aws_client

def extract_receipt_fields(request: DocumentExtractionRequest, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    textract_client = get_aws_client("textract", region_name=config.get("aws_region"))

    response = textract_client.analyze_expense(Document={"Bytes": request.document_bytes})

    receipts = []
    for document in response["ExpenseDocuments"]:
        fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document["SummaryFields"]}
        items: List[LineItem] = []
        for group in document.get("LineItemGroups", []):
            for item_data in group["LineItems"]:
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item_data["LineItemExpenseFields"]}
                items.append(LineItem(description=values.get("ITEM"), quantity=values.get("QUANTITY"), amount=values.get("PRICE")))
        
        receipts.append(ReceiptFields(
            merchant=fields.get("MERCHANT_NAME"),
            tax=fields.get("TOTAL_TAX"),
            total=fields.get("TOTAL"),
            items=items
        ).dict())

    return {"receipts": receipts}
