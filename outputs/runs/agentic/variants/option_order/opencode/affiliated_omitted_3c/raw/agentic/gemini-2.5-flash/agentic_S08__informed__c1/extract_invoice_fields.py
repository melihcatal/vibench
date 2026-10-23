import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(document_path: str) -> dict:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=f,
            content_type="application/octet-stream",
        )
        invoices = poller.result()

    extracted_data = {}
    if invoices.documents:
        invoice = invoices.documents[0]
        if invoice.fields:
            if "VendorName" in invoice.fields and invoice.fields["VendorName"]:
                extracted_data["vendor_name"] = invoice.fields["VendorName"].value
            if "InvoiceDate" in invoice.fields and invoice.fields["InvoiceDate"]:
                extracted_data["invoice_date"] = str(
                    invoice.fields["InvoiceDate"].value
                )
            if "InvoiceTotal" in invoice.fields and invoice.fields["InvoiceTotal"]:
                extracted_data["invoice_total"] = invoice.fields[
                    "InvoiceTotal"
                ].value.amount
            if "LineItems" in invoice.fields and invoice.fields["LineItems"]:
                extracted_data["line_items"] = []
                for item in invoice.fields["LineItems"].value:
                    line_item = {}
                    if "Description" in item.value and item.value["Description"]:
                        line_item["description"] = item.value["Description"].value
                    if "Amount" in item.value and item.value["Amount"]:
                        line_item["amount"] = item.value["Amount"].value
                    extracted_data["line_items"].append(line_item)
    return extracted_data
