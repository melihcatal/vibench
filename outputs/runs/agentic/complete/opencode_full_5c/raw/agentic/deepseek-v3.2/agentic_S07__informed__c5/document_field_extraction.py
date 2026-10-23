import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import FieldExtractionResult


def extract_invoice_fields(image_path: str) -> FieldExtractionResult:
    """Extract structured fields from OCR-normalized document text using Azure Document Intelligence prebuilt invoice."""
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Please set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables"
        )

    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    with open(image_path, "rb") as f:
        image_data = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=image_data,
        content_type="application/octet-stream",
    )

    result = poller.result()

    fields = {}
    confidence_scores = {}

    if hasattr(result, "documents") and result.documents:
        document = result.documents[0]

        field_mapping = {
            "VendorName": "vendor_name",
            "VendorAddress": "vendor_address",
            "CustomerName": "customer_name",
            "CustomerAddress": "customer_address",
            "InvoiceId": "invoice_id",
            "InvoiceDate": "invoice_date",
            "DueDate": "due_date",
            "TotalAmount": "total_amount",
            "SubTotal": "subtotal",
            "Tax": "tax",
            "AmountDue": "amount_due",
        }

        for field_name, field_value in document.fields.items():
            normalized_name = field_mapping.get(field_name, field_name.lower())

            if field_value and hasattr(field_value, "content"):
                fields[normalized_name] = field_value.content

                if hasattr(field_value, "confidence"):
                    confidence_scores[normalized_name] = field_value.confidence

    return FieldExtractionResult(
        fields=fields, confidence_scores=confidence_scores, raw_response=result
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python document_field_extraction.py <image_path>")
        sys.exit(1)

    result = extract_invoice_fields(sys.argv[1])

    print("Extracted invoice fields:")
    for field_name, field_value in result.fields.items():
        confidence = result.confidence_scores.get(field_name, 0.0)
        print(f"  {field_name}: {field_value} (confidence: {confidence:.2f})")
