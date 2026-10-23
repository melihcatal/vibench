from document_client import get_document_intelligence_client
from document_models import ExtractedInvoice, LineItem
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_invoice_fields(document_url: str) -> ExtractedInvoice:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document_from_url("prebuilt-invoice", document_url)
    result: AnalyzeResult = poller.result()

    invoice_fields = ExtractedInvoice()
    if result.documents and result.documents[0].fields:
        doc_fields = result.documents[0].fields

        invoice_fields.vendor_name = (
            doc_fields.get("VendorName") and doc_fields["VendorName"].value_string
        )
        invoice_fields.invoice_date = (
            doc_fields.get("InvoiceDate")
            and doc_fields["InvoiceDate"].value_date.isoformat()
            if doc_fields["InvoiceDate"].value_date
            else None
        )
        invoice_fields.total_amount = (
            doc_fields.get("InvoiceTotal")
            and doc_fields["InvoiceTotal"].value_currency
            and doc_fields["InvoiceTotal"].value_currency.amount
        )
        invoice_fields.currency = (
            doc_fields.get("InvoiceTotal")
            and doc_fields["InvoiceTotal"].value_currency
            and doc_fields["InvoiceTotal"].value_currency.currency_symbol
        )
        invoice_fields.vendor_notes = (
            doc_fields.get("CustomerNotes") and doc_fields["CustomerNotes"].value_string
        )

        if doc_fields.get("Items") and doc_fields["Items"].value_array:
            for item_field in doc_fields["Items"].value_array:
                if item_field.value_object:
                    item = item_field.value_object
                    invoice_fields.line_items.append(
                        LineItem(
                            description=item.get("Description")
                            and item["Description"].value_string,
                            quantity=item.get("Quantity")
                            and item["Quantity"].value_number,
                            unit_price=item.get("UnitPrice")
                            and item["UnitPrice"].value_currency
                            and item["UnitPrice"].value_currency.amount,
                            total_price=item.get("Amount")
                            and item["Amount"].value_currency
                            and item["Amount"].value_currency.amount,
                        )
                    )
    return invoice_fields
