import os
import boto3
from document_client import get_textract_client
from document_models import ExtractedReceiptFields, LineItem


def extract_receipt_fields(file_content: bytes) -> ExtractedReceiptFields:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    client = get_textract_client()

    # Assuming input is a JPEG or PNG image for AnalyzeExpense
    # For PDF, you would use start_document_analysis and get_document_analysis results
    response = client.analyze_expense(Document={"Bytes": file_content})

    extracted_fields = ExtractedReceiptFields()

    # Textract AnalyzeExpense response structure is different from Document AI
    # It provides summary fields and line item details under ExpenseDocuments
    if response.get("ExpenseDocuments"):
        for doc in response["ExpenseDocuments"]:
            # Extract summary fields
            if doc.get("SummaryFields"):
                for field in doc["SummaryFields"]:
                    if field.get("Type", {}).get("Text") == "VENDOR_NAME" and field.get(
                        "ValueDetection"
                    ):
                        extracted_fields.merchant_name = field["ValueDetection"]["Text"]
                        extracted_fields.confidence = max(
                            extracted_fields.confidence,
                            field["ValueDetection"]["Confidence"] / 100,
                        )
                    elif field.get("Type", {}).get("Text") == "DATE" and field.get(
                        "ValueDetection"
                    ):
                        extracted_fields.transaction_date = field["ValueDetection"][
                            "Text"
                        ]
                        extracted_fields.confidence = max(
                            extracted_fields.confidence,
                            field["ValueDetection"]["Confidence"] / 100,
                        )
                    elif field.get("Type", {}).get("Text") == "TOTAL_TAX" and field.get(
                        "ValueDetection"
                    ):
                        try:
                            extracted_fields.tax_amount = float(
                                field["ValueDetection"]["Text"]
                            )
                            extracted_fields.confidence = max(
                                extracted_fields.confidence,
                                field["ValueDetection"]["Confidence"] / 100,
                            )
                        except ValueError:
                            pass
                    elif field.get("Type", {}).get("Text") == "TOTAL" and field.get(
                        "ValueDetection"
                    ):
                        try:
                            extracted_fields.total_amount = float(
                                field["ValueDetection"]["Text"]
                            )
                            extracted_fields.confidence = max(
                                extracted_fields.confidence,
                                field["ValueDetection"]["Confidence"] / 100,
                            )
                        except ValueError:
                            pass

            # Extract line items
            if doc.get("LineItemGroups"):
                for item_group in doc["LineItemGroups"]:
                    if item_group.get("LineItems"):
                        for item in item_group["LineItems"]:
                            new_line_item = LineItem(description="")
                            if item.get("LineItemExpenseFields"):
                                for field in item["LineItemExpenseFields"]:
                                    if field.get("Type", {}).get(
                                        "Text"
                                    ) == "ITEM_DESCRIPTION" and field.get(
                                        "ValueDetection"
                                    ):
                                        new_line_item.description = field[
                                            "ValueDetection"
                                        ]["Text"]
                                    elif field.get("Type", {}).get(
                                        "Text"
                                    ) == "QUANTITY" and field.get("ValueDetection"):
                                        try:
                                            new_line_item.quantity = float(
                                                field["ValueDetection"]["Text"]
                                            )
                                        except ValueError:
                                            pass
                                    elif field.get("Type", {}).get(
                                        "Text"
                                    ) == "PRICE" and field.get("ValueDetection"):
                                        try:
                                            new_line_item.unit_price = float(
                                                field["ValueDetection"]["Text"]
                                            )
                                        except ValueError:
                                            pass
                                    elif field.get("Type", {}).get(
                                        "Text"
                                    ) == "TOTAL" and field.get("ValueDetection"):
                                        try:
                                            new_line_item.total_price = float(
                                                field["ValueDetection"]["Text"]
                                            )
                                        except ValueError:
                                            pass
                            extracted_fields.line_items.append(new_line_item)

    return extracted_fields
