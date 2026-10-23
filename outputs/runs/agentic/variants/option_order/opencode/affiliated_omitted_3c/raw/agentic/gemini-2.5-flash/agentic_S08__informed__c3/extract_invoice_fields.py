import io
from typing import Optional, List
from document_client import get_document_intelligence_client
from document_models import ExtractedInvoice, ExtractedField, InvoiceLineItem
from azure.ai.formrecognizer import AnalyzeResult


def extract_invoice_fields(invoice_data: bytes) -> ExtractedInvoice:
    document_analysis_client = get_document_intelligence_client()

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", invoice_data
    )
    invoices: AnalyzeResult = poller.result()

    if not invoices.documents:
        return ExtractedInvoice()

    invoice = invoices.documents[0]

    vendor_name = (
        ExtractedField(
            invoice.fields.get("VendorName").content,
            invoice.fields.get("VendorName").confidence,
        )
        if invoice.fields.get("VendorName")
        else None
    )
    invoice_date = (
        ExtractedField(
            str(invoice.fields.get("InvoiceDate").value),
            invoice.fields.get("InvoiceDate").confidence,
        )
        if invoice.fields.get("InvoiceDate")
        else None
    )
    total_amount = (
        ExtractedField(
            invoice.fields.get("InvoiceTotal").value,
            invoice.fields.get("InvoiceTotal").confidence,
        )
        if invoice.fields.get("InvoiceTotal")
        else None
    )

    line_items: List[InvoiceLineItem] = []
    if invoice.fields.get("Items") and invoice.fields.get("Items").value:
        for item in invoice.fields.get("Items").value:
            item_description = (
                item.value.get("Description").value
                if item.value.get("Description")
                else None
            )
            item_quantity = (
                item.value.get("Quantity").value if item.value.get("Quantity") else None
            )
            item_unit_price = (
                item.value.get("UnitPrice").value
                if item.value.get("UnitPrice")
                else None
            )
            item_amount = (
                item.value.get("Amount").value if item.value.get("Amount") else None
            )
            line_items.append(
                InvoiceLineItem(
                    description=item_description,
                    quantity=item_quantity,
                    unit_price=item_unit_price,
                    amount=item_amount,
                )
            )

    vendor_address = (
        ExtractedField(
            invoice.fields.get("VendorAddress").content,
            invoice.fields.get("VendorAddress").confidence,
        )
        if invoice.fields.get("VendorAddress")
        else None
    )
    customer_name = (
        ExtractedField(
            invoice.fields.get("CustomerName").content,
            invoice.fields.get("CustomerName").confidence,
        )
        if invoice.fields.get("CustomerName")
        else None
    )
    purchase_order = (
        ExtractedField(
            invoice.fields.get("PurchaseOrder").content,
            invoice.fields.get("PurchaseOrder").confidence,
        )
        if invoice.fields.get("PurchaseOrder")
        else None
    )
    due_date = (
        ExtractedField(
            str(invoice.fields.get("DueDate").value),
            invoice.fields.get("DueDate").confidence,
        )
        if invoice.fields.get("DueDate")
        else None
    )
    currency = (
        ExtractedField(
            invoice.fields.get("Currency").value,
            invoice.fields.get("Currency").confidence,
        )
        if invoice.fields.get("Currency")
        else None
    )
    invoice_id = (
        ExtractedField(
            invoice.fields.get("InvoiceId").content,
            invoice.fields.get("InvoiceId").confidence,
        )
        if invoice.fields.get("InvoiceId")
        else None
    )
    subtotal = (
        ExtractedField(
            invoice.fields.get("SubTotal").value,
            invoice.fields.get("SubTotal").confidence,
        )
        if invoice.fields.get("SubTotal")
        else None
    )
    total_tax = (
        ExtractedField(
            invoice.fields.get("TotalTax").value,
            invoice.fields.get("TotalTax").confidence,
        )
        if invoice.fields.get("TotalTax")
        else None
    )

    return ExtractedInvoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items,
        vendor_address=vendor_address,
        customer_name=customer_name,
        purchase_order=purchase_order,
        due_date=due_date,
        currency=currency,
        invoice_id=invoice_id,
        subtotal=subtotal,
        total_tax=total_tax,
    )
