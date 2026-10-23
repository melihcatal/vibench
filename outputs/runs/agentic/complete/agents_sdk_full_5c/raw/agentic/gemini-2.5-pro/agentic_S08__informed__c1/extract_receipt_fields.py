from document_client import get_mindee_client
from document_models import Receipt, ReceiptLineItem

def extract_receipt_fields(file_path: str) -> Receipt:
    """
    Extracts structured data from a receipt using the Mindee API.
    """
    mindee_client = get_mindee_client()
    input_doc = mindee_client.source_from_path(file_path)
    
    # Use the Mindee Receipt OCR product
    result = mindee_client.parse(
        product_class=mindee_client.products.ReceiptV5,
        input_source=input_doc,
    )
    
    doc_prediction = result.document.inference.prediction
    
    line_items = []
    if doc_prediction.line_items:
        for item in doc_prediction.line_items:
            line_items.append(
                ReceiptLineItem(
                    description=item.description,
                    quantity=item.quantity,
                    total_price=item.total_amount,
                )
            )

    return Receipt(
        merchant_name=doc_prediction.supplier_name.value if doc_prediction.supplier_name else None,
        receipt_date=str(doc_prediction.date.value) if doc_prediction.date else None,
        total_amount=doc_prediction.total_amount.value if doc_prediction.total_amount else None,
        tax_amount=doc_prediction.total_tax.value if doc_prediction.total_tax else None,
        items=line_items,
        raw_response=result.document.to_dict()
    )
