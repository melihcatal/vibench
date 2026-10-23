import os
import boto3
from document_models import ExtractedReceipt, LineItem
from document_client import get_textract_client


def extract_receipt_fields(file_content: bytes) -> ExtractedReceipt:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    client = get_textract_client()

    response = client.analyze_expense(Document={"Bytes": file_content})

    extracted_receipt = ExtractedReceipt(
        raw_text=" ".join(
            [block["Text"] for block in response.get("Blocks", []) if "Text" in block]
        )
    )

    for expense_document in response["ExpenseDocuments"]:
        for field in expense_document["SummaryFields"]:
            if field["Type"]["Text"] == "MERCHANT_NAME":
                extracted_receipt.merchant_name = field["ValueDetection"]["Text"]
            elif field["Type"]["Text"] == "DATE":
                extracted_receipt.transaction_date = field["ValueDetection"]["Text"]
            elif field["Type"]["Text"] == "TOTAL":
                extracted_receipt.total_amount = (
                    float(field["ValueDetection"]["Text"])
                    if field["ValueDetection"]["Text"]
                    else None
                )
                extracted_receipt.currency = (
                    field["Currency"]["Text"] if "Currency" in field else None
                )
            elif field["Type"]["Text"] == "TAX":
                extracted_receipt.tax_amount = (
                    float(field["ValueDetection"]["Text"])
                    if field["ValueDetection"]["Text"]
                    else None
                )

        for line_item_group in expense_document["LineItemGroups"]:
            for line_item_field in line_item_group["LineItems"]:
                description = None
                quantity = None
                unit_price = None
                total_price = None
                for field in line_item_field["LineItemExpenseFields"]:
                    if field["Type"]["Text"] == "ITEM":
                        description = field["ValueDetection"]["Text"]
                    elif field["Type"]["Text"] == "QUANTITY":
                        quantity = (
                            float(field["ValueDetection"]["Text"])
                            if field["ValueDetection"]["Text"]
                            else None
                        )
                    elif field["Type"]["Text"] == "UNIT_PRICE":
                        unit_price = (
                            float(field["ValueDetection"]["Text"])
                            if field["ValueDetection"]["Text"]
                            else None
                        )
                    elif field["Type"]["Text"] == "PRICE":  # Total for the line item
                        total_price = (
                            float(field["ValueDetection"]["Text"])
                            if field["ValueDetection"]["Text"]
                            else None
                        )
                if description:
                    extracted_receipt.items.append(
                        LineItem(
                            description=description,
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=total_price,
                        )
                    )

    return extracted_receipt
