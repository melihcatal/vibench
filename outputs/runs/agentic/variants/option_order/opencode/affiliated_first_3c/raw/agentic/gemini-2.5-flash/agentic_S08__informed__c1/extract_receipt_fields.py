import base64
import datetime
from typing import Dict, Any
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, ReceiptExtractionResult, LineItem


def extract_receipt_fields(
    request: DocumentExtractionRequest,
) -> ReceiptExtractionResult:
    client = DocumentClient()

    # The raw document bytes
    document_bytes = base64.b64decode(request.document_content)

    response = client.textract_client.analyze_expense(
        Document={"Bytes": document_bytes}
    )

    merchant_name = None
    transaction_date = None
    tax_amount = None
    total_amount = None
    currency = None
    line_items = []

    if response.get("ExpenseDocuments"):
        expense_document = response["ExpenseDocuments"][0]
        if expense_document.get("SummaryFields"):
            for field in expense_document["SummaryFields"]:
                if field["Type"]["Text"] == "VENDOR_NAME" and "ValueDetection" in field:
                    merchant_name = field["ValueDetection"]["Text"]
                elif field["Type"]["Text"] == "DATE" and "ValueDetection" in field:
                    try:
                        transaction_date = datetime.datetime.strptime(
                            field["ValueDetection"]["Text"], "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        pass
                elif field["Type"]["Text"] == "TAX" and "ValueDetection" in field:
                    try:
                        tax_amount = float(field["ValueDetection"]["Text"])
                    except ValueError:
                        pass
                elif field["Type"]["Text"] == "TOTAL" and "ValueDetection" in field:
                    try:
                        total_amount = float(field["ValueDetection"]["Text"])
                        if "Currency" in field["ValueDetection"]:
                            currency = field["ValueDetection"]["Currency"]
                    except ValueError:
                        pass
        if expense_document.get("LineItemGroups"):
            for item_group in expense_document["LineItemGroups"]:
                for item_field in item_group.get("LineItems", []):
                    line_item = LineItem()
                    for field in item_field.get("LineItemExpenseFields", []):
                        if (
                            field["Type"]["Text"] == "ITEM_DESCRIPTION"
                            and "ValueDetection" in field
                        ):
                            line_item.description = field["ValueDetection"]["Text"]
                        elif (
                            field["Type"]["Text"] == "QUANTITY"
                            and "ValueDetection" in field
                        ):
                            try:
                                line_item.quantity = float(
                                    field["ValueDetection"]["Text"]
                                )
                            except ValueError:
                                pass
                        elif (
                            field["Type"]["Text"] == "UNIT_PRICE"
                            and "ValueDetection" in field
                        ):
                            try:
                                line_item.unit_price = float(
                                    field["ValueDetection"]["Text"]
                                )
                            except ValueError:
                                pass
                        elif (
                            field["Type"]["Text"] == "PRICE"
                            and "ValueDetection" in field
                        ):
                            try:
                                line_item.total_price = float(
                                    field["ValueDetection"]["Text"]
                                )
                            except ValueError:
                                pass
                    if line_item.description or line_item.total_price:
                        line_items.append(line_item)

    return ReceiptExtractionResult(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_response=response,
    )
