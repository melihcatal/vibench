import os
from typing import Optional, Dict, Any
from mindee import Client, InvoiceV4Document
from document_models import DocumentTextResult


MINDEE_INVOICE_MODEL = "invoice"


def extract_document_fields(
    ocr_result: DocumentTextResult,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    mindee_api_key = os.environ.get("MINDEE_API_KEY")
    if not mindee_api_key:
        raise ValueError("MINDEE_API_KEY environment variable must be set")

    mindee_client = Client(api_key=mindee_api_key)

    if image_path:
        with open(image_path, "rb") as f:
            input_doc = mindee_client.source_from_file(f)
    elif image_bytes:
        input_doc = mindee_client.source_from_bytes(image_bytes)
    else:
        raise ValueError("Either image_path or image_bytes must be provided")

    result = mindee_client.parse(
        InvoiceV4Document,
        input_doc,
    )

    document = result.document
    fields = {}

    if document.invoice_number:
        fields["invoice_number"] = document.invoice_number.value

    if document.date:
        fields["date"] = document.date.value

    if document.due_date:
        fields["due_date"] = document.due_date.value

    if document.total_amount:
        fields["total_amount"] = document.total_amount.value

    if document.total_net:
        fields["total_net"] = document.total_net.value

    if document.total_tax:
        fields["total_tax"] = document.total_tax.value

    if document.currency:
        fields["currency"] = document.currency.value

    if document.supplier:
        supplier_fields = {}
        if document.supplier.name:
            supplier_fields["name"] = document.supplier.name.value
        if document.supplier.address:
            supplier_fields["address"] = document.supplier.address.value
        if document.supplier.company_registrations:
            supplier_fields["registrations"] = [
                reg.value for reg in document.supplier.company_registrations
            ]
        if supplier_fields:
            fields["supplier"] = supplier_fields

    if document.customer:
        customer_fields = {}
        if document.customer.name:
            customer_fields["name"] = document.customer.name.value
        if document.customer.address:
            customer_fields["address"] = document.customer.address.value
        if customer_fields:
            fields["customer"] = customer_fields

    if document.line_items:
        line_items = []
        for item in document.line_items:
            item_data = {}
            if item.description:
                item_data["description"] = item.description
            if item.quantity:
                item_data["quantity"] = item.quantity
            if item.unit_price:
                item_data["unit_price"] = item.unit_price
            if item.total_amount:
                item_data["total_amount"] = item.total_amount
            if item_data:
                line_items.append(item_data)
        if line_items:
            fields["line_items"] = line_items

    if document.taxes:
        taxes = []
        for tax in document.taxes:
            tax_data = {}
            if tax.rate:
                tax_data["rate"] = tax.rate
            if tax.base:
                tax_data["base"] = tax.base
            if tax.amount:
                tax_data["amount"] = tax.amount
            if tax_data:
                taxes.append(tax_data)
        if taxes:
            fields["taxes"] = taxes

    return fields


if __name__ == "__main__":
    image_file = os.environ.get("DOCUMENT_IMAGE_PATH")
    if image_file:
        sample_ocr = DocumentTextResult(raw_text="", lines=[], confidence=1.0)
        fields = extract_document_fields(sample_ocr, image_path=image_file)
        for key, value in fields.items():
            print(f"{key}: {value}")
