import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Any

def extract_structured_fields_from_invoice(document_path: str) -> Dict[str, Any]:
    """
    Extracts structured fields from an invoice document using Azure Document Intelligence's prebuilt invoice model.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-invoice", document=f.read()
        )
        result = poller.result()

    invoice_fields = {}
    if result.documents:
        invoice = result.documents[0]
        for field_name, field_value in invoice.fields.items():
            invoice_fields[field_name] = {
                "content": field_value.content if field_value else None,
                "value": field_value.value if field_value else None, # The interpreted value if available
                "confidence": field_value.confidence if field_value else None
            }
    return invoice_fields

if __name__ == '__main__':
    # Example usage (requires environment variables set and an invoice document)
    # invoice_data = extract_structured_fields_from_invoice("path/to/your/invoice.pdf")
    # for field_name, field_info in invoice_data.items():
    #     print(f"Field: {field_name}, Content: {field_info['content']}, Value: {field_info['value']}, Confidence: {field_info['confidence']}")
    pass
