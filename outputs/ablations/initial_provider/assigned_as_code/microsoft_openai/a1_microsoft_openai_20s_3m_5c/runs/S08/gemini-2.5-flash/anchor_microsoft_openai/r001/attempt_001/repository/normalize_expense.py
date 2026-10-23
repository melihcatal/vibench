from document_models import ExtractedDocument, NormalizedExpense, LineItem

def normalize_expense(extracted_document: ExtractedDocument, document_type: str) -> NormalizedExpense:
    normalized_line_items = []
    source_line_items = extracted_document.line_items if document_type == "invoice" else extracted_document.items
    
    for item in source_line_items:
        normalized_line_items.append(LineItem(
            description=item.description,
            quantity=item.quantity,
            amount=item.amount
        ))

    vendor_name = extracted_document.vendor_name if extracted_document.vendor_name else extracted_document.merchant_name
    total_amount = extracted_document.total
    transaction_date = extracted_document.date

    return NormalizedExpense(
        transaction_date=transaction_date,
        vendor=vendor_name,
        total_amount=total_amount,
        line_items=normalized_line_items,
        original_document_type=document_type
    )
