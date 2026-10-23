import os
from mindee import Client, product
from document_client import DocumentAIClient
from document_models import InvoiceFields, LineItem, ExtractionResult

def extract_invoice_fields(file_path: str) -> ExtractionResult:
    client = DocumentAIClient().get_mindee_client()

    with open(file_path, "rb") as file_handle:
        input_doc = client.doc_from_file(file_handle)

    response = input_doc.parse(product.InvoiceV4)
    invoice = response.document.inference.prediction

    if response.document.inference.is_prediction_available:
        extracted_line_items = []
        for item in invoice.line_items:
            extracted_line_items.append(LineItem(
                description=item.description.value,
                quantity=item.quantity.value,
                unit_price=item.unit_price.value,
                total=item.total_amount.value
            ))

        invoice_fields = InvoiceFields(
            vendor_name=invoice.supplier_name.value,
            invoice_date=invoice.date.value,
            total_amount=invoice.total_amount.value,
            currency=invoice.total_amount.currency,
            line_items=extracted_line_items
        )
        return ExtractionResult(
            success=True,
            data=invoice_fields.to_dict(),
            confidence=response.document.inference.prediction.total_amount.confidence
        )
    else:
        return ExtractionResult(
            success=False,
            error="Mindee failed to extract invoice fields."
        )
