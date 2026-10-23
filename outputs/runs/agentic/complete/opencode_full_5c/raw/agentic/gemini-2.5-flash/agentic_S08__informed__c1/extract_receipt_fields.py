from mindee import Client, product
from document_client import get_mindee_client
from document_models import ExtractedReceipt, LineItem
import base64


def extract_receipt_fields(image_content: bytes) -> ExtractedReceipt:
    mindee_client: Client = get_mindee_client()

    input_doc = mindee_client.doc_from_bytes(image_content, "receipt.pdf")
    result = mindee_client.parse(product.ReceiptV5, input_doc)

    receipt_prediction = result.document.inference.prediction

    line_items = []
    for item in receipt_prediction.line_items:
        line_items.append(
            LineItem(
                description=item.description.value if item.description else None,
                quantity=item.quantity.value if item.quantity else None,
                unit_price=item.unit_price.value if item.unit_price else None,
                total_price=item.total_amount.value if item.total_amount else None,
            )
        )

    return ExtractedReceipt(
        merchant_name=receipt_prediction.supplier_name.value
        if receipt_prediction.supplier_name
        else None,
        transaction_date=receipt_prediction.date.value
        if receipt_prediction.date
        else None,
        total_amount=receipt_prediction.total_amount.value
        if receipt_prediction.total_amount
        else None,
        tax_amount=receipt_prediction.total_tax.value
        if receipt_prediction.total_tax
        else None,
        line_items=line_items,
        currency=receipt_prediction.total_amount.currency.value
        if receipt_prediction.total_amount and receipt_prediction.total_amount.currency
        else None,
    )
