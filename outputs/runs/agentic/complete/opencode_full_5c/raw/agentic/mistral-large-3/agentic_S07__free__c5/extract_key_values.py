from typing import Dict, List, Optional
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import (
    get_azure_form_recognizer_client,
    get_azure_form_recognizer_endpoint,
)
from document_models import KeyValueResponse


def extract_key_values(image_path: str) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Azure Form Recognizer."""
    endpoint = get_azure_form_recognizer_endpoint()
    credential = AzureKeyCredential(os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
    client = get_azure_form_recognizer_client()

    with open(image_path, "rb") as image_file:
        poller = client.begin_analyze_document("prebuilt-document", image_file)

    result = poller.result()
    key_values = []

    for kv_pair in result.key_value_pairs:
        key = kv_pair.key.content if kv_pair.key else ""
        value = kv_pair.value.content if kv_pair.value else ""

        key_values.append(
            {
                "key": key,
                "value": value,
                "confidence": kv_pair.confidence,
                "key_bounding_box": [
                    {"x": point.x, "y": point.y}
                    for point in kv_pair.key.bounding_regions[0].polygon
                ]
                if kv_pair.key and kv_pair.key.bounding_regions
                else [],
                "value_bounding_box": [
                    {"x": point.x, "y": point.y}
                    for point in kv_pair.value.bounding_regions[0].polygon
                ]
                if kv_pair.value and kv_pair.value.bounding_regions
                else [],
            }
        )

    return KeyValueResponse(key_value_pairs=key_values)
