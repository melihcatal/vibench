import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_form_recognizer_client
from document_models import (
    KeyValueExtractionRequest,
    KeyValueExtractionResponse,
    KeyValuePair,
)


def extract_key_values(
    request: KeyValueExtractionRequest,
) -> KeyValueExtractionResponse:
    """Extract key-value pairs from a form-like document using Azure Form Recognizer."""
    client = get_form_recognizer_client()

    with open(request.document_path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id="prebuilt-document", document=document
        )

    result = poller.result()

    key_values = []

    if hasattr(result, "key_value_pairs"):
        for kv in result.key_value_pairs:
            key = kv.key.content if kv.key else ""
            value = kv.value.content if kv.value else ""
            confidence = min(
                kv.key.confidence if kv.key and hasattr(kv.key, "confidence") else 0.9,
                kv.value.confidence
                if kv.value and hasattr(kv.value, "confidence")
                else 0.9,
            )

            key_values.append(
                KeyValuePair(
                    key=key,
                    value=value,
                    confidence=confidence,
                    bounding_box=kv.bounding_box
                    if hasattr(kv, "bounding_box")
                    else None,
                )
            )

    return KeyValueExtractionResponse(
        key_values=key_values,
        provider="azure-form-recognizer",
        model_id="prebuilt-document",
        raw_response=result,
    )
