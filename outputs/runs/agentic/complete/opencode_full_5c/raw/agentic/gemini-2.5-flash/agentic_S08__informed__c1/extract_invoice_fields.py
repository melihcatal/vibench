from mindee import Client, product
from document_client import get_mindee_client
from document_models import ExtractedInvoice, LineItem
import base64


def extract_invoice_fields(image_content: bytes) -> ExtractedInvoice:
    mindee_client: Client = get_mindee_client()

    # Mindee expects a file-like object or path. We'll write to a temp file or use base64 if supported.
    # For simplicity, we'll assume a path or bytes directly can be passed,
    # but a real implementation might need a temporary file.
    # Mindee SDK's parse method can take `file` which can be bytes.

    # To fulfill the Mindee SDK requirement for file-like object,
    # we might need to save image_content to a temporary file, then pass the path or open the file in memory.
    # For this example, let's try to pass bytes directly if the SDK allows or simulate a file upload.

    # The Mindee Python SDK `parse` method takes `file` parameter which can be a `bytes` object.
    input_doc = mindee_client.doc_from_bytes(image_content, "invoice.pdf")
    result = mindee_client.parse(product.InvoiceV4, input_doc)

    invoice_prediction = result.document.inference.prediction

    line_items = []
    for item in invoice_prediction.line_items:
        line_items.append(
            LineItem(
                description=item.description.value if item.description else None,
                quantity=item.quantity.value if item.quantity else None,
                unit_price=item.unit_price.value if item.unit_price else None,
                total_price=item.total_amount.value if item.total_amount else None,
            )
        )

    return ExtractedInvoice(
        vendor_name=invoice_prediction.supplier_name.value
        if invoice_prediction.supplier_name
        else None,
        invoice_date=invoice_prediction.date.value if invoice_prediction.date else None,
        total_amount=invoice_prediction.total_amount.value
        if invoice_prediction.total_amount
        else None,
        line_items=line_items,
        currency=invoice_prediction.total_amount.currency.value
        if invoice_prediction.total_amount and invoice_prediction.total_amount.currency
        else None,
        invoice_number=invoice_prediction.invoice_number.value
        if invoice_prediction.invoice_number
        else None,
        purchase_order=invoice_prediction.reference.value
        if invoice_prediction.reference
        else None,  # Using reference as purchase order for Mindee InvoiceV4
    )
