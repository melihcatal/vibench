import os
import boto3
from document_models import ReceiptExtract, ExtractedField, LineItem, Confidence
from document_client import load_image_bytes


def extract_receipt_fields(image_path: str) -> ReceiptExtract:
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError("Missing AWS credentials env vars")
    textract = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
    image_bytes = load_image_bytes(image_path)
    response = textract.analyze_expense(
        Document={"Bytes": image_bytes}, FeatureTypes=["EXPENSE_RECEIPTS"]
    )
    if not response.get("ExpenseDocuments"):
        raise ValueError("No receipt document processed")
    doc = response["ExpenseDocuments"][0]
    fields_map = {f["Type"]["Text"]: f for f in doc["ExpenseFields"]}
    merchant_data = fields_map.get("MERCHANT_NAME", {})
    merchant_field = ExtractedField(
        content=merchant_data.get("Text", ""),
        confidence=Confidence(value=merchant_data.get("Confidence", 0.0)),
    )
    date_data = fields_map.get("TRANSACTION_DATE", {}) or fields_map.get(
        "INVOICE_DATE", {}
    )
    date_field = ExtractedField(
        content=date_data.get("Text", ""),
        confidence=Confidence(value=date_data.get("Confidence", 0.0)),
    )
    tax_data = fields_map.get("TAX_TOTAL", {})
    tax_field = ExtractedField(
        content=tax_data.get("Text", "0"),
        confidence=Confidence(value=tax_data.get("Confidence", 0.0)),
    )
    total_data = fields_map.get("TOTAL", {})
    total_field = ExtractedField(
        content=total_data.get("Text", "0"),
        confidence=Confidence(value=total_data.get("Confidence", 0.0)),
    )
    items = []
    if "LineItemGroups" in doc:
        for group in doc["LineItemGroups"]:
            for line_item in group.get("LineItems", []):
                description = ""
                if "Item" in line_item:
                    for item_field in line_item["Item"]:
                        if (
                            item_field["Type"]["Text"] == "NAME"
                            or item_field["Type"]["Text"] == "DESCRIPTION"
                        ):
                            description = item_field["Text"]
                            break
                price_data = next(
                    (
                        p
                        for p in line_item.get("Price", [])
                        if p["Type"]["Text"] == "ITEM_PRICE"
                    ),
                    {},
                )
                price = (
                    float(price_data.get("Text", "0").replace("$", "").replace(",", ""))
                    if price_data.get("Text")
                    else 0.0
                )
                conf = price_data.get("Confidence", 0.8)
                items.append(
                    LineItem(
                        description=description,
                        total_price=price,
                        confidence=Confidence(value=conf),
                    )
                )
    return ReceiptExtract(
        merchant_name=merchant_field,
        transaction_date=date_field,
        tax_amount=tax_field,
        total_amount=total_field,
        items=items,
        raw_response=response,
    )
