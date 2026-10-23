import os
from typing import List, Dict, Any, Optional
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_client
from document_models import KeyValuePair, KeyValueExtractionResult


def extract_key_values(
    image_path: str, document_type: Optional[str] = None
) -> KeyValueExtractionResult:
    """
    Extract key-value pairs from a form-like document using Azure Form Recognizer.

    Args:
        image_path: Path to the image file
        document_type: Optional document type hint (e.g., 'invoice', 'receipt')

    Returns:
        KeyValueExtractionResult containing extracted key-value pairs
    """
    client = get_azure_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    model_id = "prebuilt-document"
    if document_type == "invoice":
        model_id = "prebuilt-invoice"
    elif document_type == "receipt":
        model_id = "prebuilt-receipt"
    elif document_type == "idDocument":
        model_id = "prebuilt-idDocument"

    poller = client.begin_analyze_document(model_id=model_id, document=image_data)

    result = poller.result()

    key_values = []

    for field_name, field in result.documents[0].fields.items():
        if field.value:
            key_values.append(
                KeyValuePair(
                    key=field_name,
                    value=str(field.value),
                    confidence=field.confidence,
                    bounding_box=field.bounding_box
                    if hasattr(field, "bounding_box")
                    else None,
                )
            )

    return KeyValueExtractionResult(
        key_values=key_values,
        provider="azure_form_recognizer",
        model_id=model_id,
        document_type=document_type,
    )
