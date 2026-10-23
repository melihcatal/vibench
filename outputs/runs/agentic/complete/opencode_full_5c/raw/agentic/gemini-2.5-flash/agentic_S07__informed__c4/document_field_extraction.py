import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_structured_fields(
    file_content: bytes, mime_type: str, model_id: str = "prebuilt-invoice"
) -> dict:
    """
    Extracts structured fields from OCR-normalized document text using Azure Document Intelligence.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set."
        )

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        model_id, file_content, content_type=mime_type
    )
    result = poller.result()

    extracted_fields = {}
    if result.documents:
        # Assuming a single document for simplicity, adjust if multiple documents are expected
        document = result.documents[0]
        for name, field in document.fields.items():
            extracted_fields[name] = {
                "content": field.content,
                "value_type": str(field.value_type),
                "confidence": field.confidence,
            }
            if field.value:
                # Add specific value properties if available
                if hasattr(field.value, "currency_symbol"):
                    extracted_fields[name]["value"] = {
                        "amount": field.value.amount,
                        "currency_symbol": field.value.currency_symbol,
                    }
                else:
                    extracted_fields[name]["value"] = field.value

    return extracted_fields
