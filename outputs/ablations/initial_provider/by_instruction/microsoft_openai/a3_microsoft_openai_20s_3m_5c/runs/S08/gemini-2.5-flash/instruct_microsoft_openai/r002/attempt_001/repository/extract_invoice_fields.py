from document_client import DocumentClients
from document_models import Invoice, LineItem
from azure.ai.documentintelligence.models import ContentFormat
from typing import BinaryIO

def extract_invoice_fields(invoice_document: BinaryIO) -> Invoice:
    clients = DocumentClients()
    if not clients.document_intelligence_client:
        raise ValueError("Azure Document Intelligence client not initialized.")

    poller = clients.document_intelligence_client.begin_analyze_document(
        "prebuilt-invoice", invoice_document, content_type="application/pdf"
    )
    result = poller.result()

    invoice_fields = Invoice(line_items=[])

    if result.documents:
        for doc in result.documents:
            if doc.doc_type == "prebuilt-invoice":
                # Extract top-level fields
                invoice_fields.vendor_name = doc.fields.get("VendorName") and doc.fields["VendorName"].content
                invoice_fields.invoice_date = doc.fields.get("InvoiceDate") and doc.fields["InvoiceDate"].content
                invoice_fields.invoice_total = doc.fields.get("InvoiceTotal") and doc.fields["InvoiceTotal"].value
                invoice_fields.currency = doc.fields.get("Currency") and doc.fields["Currency"].content
                invoice_fields.invoice_id = doc.fields.get("InvoiceId") and doc.fields["InvoiceId"].content
                invoice_fields.customer_name = doc.fields.get("CustomerName") and doc.fields["CustomerName"].content
                invoice_fields.customer_address = doc.fields.get("CustomerAddress") and doc.fields["CustomerAddress"].content
                invoice_fields.vendor_address = doc.fields.get("VendorAddress") and doc.fields["VendorAddress"].content
                invoice_fields.purchase_order = doc.fields.get("PurchaseOrder") and doc.fields["PurchaseOrder"].content
                invoice_fields.due_date = doc.fields.get("DueDate") and doc.fields["DueDate"].content
                invoice_fields.tax_amount = doc.fields.get("TotalTax") and doc.fields["TotalTax"].value
                invoice_fields.service_start_date = doc.fields.get("ServiceStartDate") and doc.fields["ServiceStartDate"].content
                invoice_fields.service_end_date = doc.fields.get("ServiceEndDate") and doc.fields["ServiceEndDate"].content
                invoice_fields.billing_address = doc.fields.get("BillingAddress") and doc.fields["BillingAddress"].content
                invoice_fields.shipping_address = doc.fields.get("ShippingAddress") and doc.fields["ShippingAddress"].content
                invoice_fields.payment_terms = doc.fields.get("PaymentTerms") and doc.fields["PaymentTerms"].content
                invoice_fields.vat_number = doc.fields.get("VatNumber") and doc.fields["VatNumber"].content
                invoice_fields.vendor_tax_id = doc.fields.get("VendorTaxId") and doc.fields["VendorTaxId"].content
                invoice_fields.customer_tax_id = doc.fields.get("CustomerTaxId") and doc.fields["CustomerTaxId"].content
                invoice_fields.bank_account_number = doc.fields.get("BankAccountNumber") and doc.fields["BankAccountNumber"].content
                invoice_fields.swift_code = doc.fields.get("SwiftCode") and doc.fields["SwiftCode"].content
                invoice_fields.iban_number = doc.fields.get("IbanNumber") and doc.fields["IbanNumber"].content
                invoice_fields.notes = doc.fields.get("Notes") and doc.fields["Notes"].content
                invoice_fields.memo = doc.fields.get("Memo") and doc.fields["Memo"].content

                # Extract line items
                if "Items" in doc.fields:
                    for item in doc.fields["Items"].value:
                        line_item = LineItem(
                            description=item.get("Description") and item["Description"].content,
                            quantity=item.get("Quantity") and item["Quantity"].value,
                            unit_price=item.get("UnitPrice") and item["UnitPrice"].value,
                            total_price=item.get("Amount") and item["Amount"].value,
                        )
                        invoice_fields.line_items.append(line_item)
    return invoice_fields
