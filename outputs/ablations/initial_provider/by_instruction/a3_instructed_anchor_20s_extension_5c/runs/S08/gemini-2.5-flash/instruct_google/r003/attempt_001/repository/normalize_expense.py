from typing import Dict, Any
from document_models import DocumentExtractionResult, ExpenseNormalizationSchema, LineItem

def normalize_expense_data(extracted_data: DocumentExtractionResult, document_type: str) -> ExpenseNormalizationSchema:
    normalized_line_items = []
    for item in extracted_data.line_items:
        normalized_line_items.append(LineItem(
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price
        ))

    # Simple confidence score example (can be expanded with actual ML model confidences)
    confidence_scores = {
        "vendor_name": 1.0 if extracted_data.vendor_name else 0.0,
        "document_date": 1.0 if extracted_data.document_date else 0.0,
        "total_amount": 1.0 if extracted_data.total_amount else 0.0,
        "line_items": 1.0 if extracted_data.line_items else 0.0,
    }

    return ExpenseNormalizationSchema(
        merchant_name=extracted_data.vendor_name,
        transaction_date=extracted_data.document_date,
        total_amount=extracted_data.total_amount,
        currency="USD", # Assuming USD for simplicity; could be extracted or configured
        line_items=normalized_line_items,
        document_type=document_type,
        validation_status="pending",
        confidence_scores=confidence_scores
    )
