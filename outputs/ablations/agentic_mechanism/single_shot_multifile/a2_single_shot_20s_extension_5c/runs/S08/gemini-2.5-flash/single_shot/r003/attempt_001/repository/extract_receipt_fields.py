import os
import base64
from document_client import get_textract_client
from document_models import DocumentExtractionRequest, NormalizedExpense, LineItem
from typing import Dict, Any, List, Optional

def extract_receipt_fields(request: DocumentExtractionRequest) -> NormalizedExpense:
    client = get_textract_client()

    response = client.analyze_expense(
        Document={
            "Bytes": request.document_bytes,
        }
    )

    merchant_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    transaction_date: Optional[str] = None
    extracted_line_items: List[LineItem] = []
    confidence_scores: List[float] = []

    for expense_doc in response.get("ExpenseDocuments", []):
        for field in expense_doc.get("SummaryFields", []):
            field_type = field.get("Type", {}).get("Text")
            value_detection = field.get("ValueDetection", {})
            
            if field_type == "MERCHANT_NAME":
                merchant_name = value_detection.get("Text")
                confidence_scores.append(field.get("Confidence", 0.0) / 100)
            elif field_type == "TOTAL":
                if value_detection.get("Text"):
                    try:
                        total_amount = float(value_detection["Text"].replace("$", "").replace(",", ""))
                    except ValueError:
                        pass
                currency = field.get("Currency", {}).get("Text")
                confidence_scores.append(field.get("Confidence", 0.0) / 100)
            elif field_type == "TAX":
                if value_detection.get("Text"):
                    try:
                        tax_amount = float(value_detection["Text"].replace("$", "").replace(",", ""))
                    except ValueError:
                        pass
                confidence_scores.append(field.get("Confidence", 0.0) / 100)
            elif field_type == "DATE":
                transaction_date = value_detection.get("Text")
                confidence_scores.append(field.get("Confidence", 0.0) / 100)
        
        for line_item_group in expense_doc.get("LineItemGroups", []):
            for item in line_item_group.get("LineItems", []):
                item_description: Optional[str] = None
                item_quantity: Optional[float] = None
                item_unit_price: Optional[float] = None
                item_total_price: Optional[float] = None

                for field in item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text")
                    value_detection = field.get("ValueDetection", {})

                    if field_type == "ITEM":
                        item_description = value_detection.get("Text")
                    elif field_type == "QUANTITY":
                        try:
                            item_quantity = float(value_detection.get("Text"))
                        except (ValueError, TypeError):
                            pass
                    elif field_type == "PRICE":
                        try:
                            item_unit_price = float(value_detection.get("Text").replace("$", "").replace(",", ""))
                        except (ValueError, TypeError):
                            pass
                    elif field_type == "TOTAL_ITEM_AMOUNT":
                        try:
                            item_total_price = float(value_detection.get("Text").replace("$", "").replace(",", ""))
                        except (ValueError, TypeError):
                            pass
                    
                    confidence_scores.append(field.get("Confidence", 0.0) / 100)

                extracted_line_items.append(
                    LineItem(
                        description=item_description,
                        quantity=item_quantity,
                        unit_price=item_unit_price,
                        total_price=item_total_price,
                    )
                )

    overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else None

    return NormalizedExpense(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=extracted_line_items,
        document_type="receipt",
        confidence_score=overall_confidence,
        raw_extraction=response,
    )