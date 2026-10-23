import os
from document_client import get_aws_textract_client


def extract_receipt_fields(receipt_document_path: str) -> dict:
    client = get_aws_textract_client()

    with open(receipt_document_path, "rb") as document:
        response = client.analyze_expense(Document={"Bytes": document.read()})

    extracted_fields = {
        "merchant_name": None,
        "tax_amount": None,
        "total_amount": None,
        "currency": None,
        "line_items": [],
    }

    if response["ExpenseDocuments"]:
        for field in response["ExpenseDocuments"][0]["SummaryFields"]:
            if field["Type"]["Text"] == "VENDOR_NAME":
                extracted_fields["merchant_name"] = field["ValueDetection"]["Text"]
            elif field["Type"]["Text"] == "TOTAL_TAX":
                extracted_fields["tax_amount"] = (
                    float(field["ValueDetection"]["Text"])
                    if field["ValueDetection"]["Text"]
                    else None
                )
            elif field["Type"]["Text"] == "TOTAL":
                extracted_fields["total_amount"] = (
                    float(field["ValueDetection"]["Text"])
                    if field["ValueDetection"]["Text"]
                    else None
                )
                extracted_fields["currency"] = field["ValueDetection"]["Text"].replace(
                    field["ValueDetection"]["Text"].strip("0123456789.,"), ""
                )  # Simple currency extraction

        if response["ExpenseDocuments"][0].get("LineItemGroups"):
            for item_group in response["ExpenseDocuments"][0]["LineItemGroups"]:
                for item in item_group["LineItems"]:
                    item_data = {}
                    for field in item["LineItemExpenseFields"]:
                        if field["Type"]["Text"] == "ITEM":
                            item_data["description"] = field["ValueDetection"]["Text"]
                        elif field["Type"]["Text"] == "PRICE":
                            item_data["total_price"] = (
                                float(field["ValueDetection"]["Text"])
                                if field["ValueDetection"]["Text"]
                                else None
                            )
                    if item_data:
                        extracted_fields["line_items"].append(item_data)

    return extracted_fields
