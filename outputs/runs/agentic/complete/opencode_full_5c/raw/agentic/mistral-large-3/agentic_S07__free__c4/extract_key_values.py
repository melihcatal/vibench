from typing import Dict, List, Optional
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_form_recognizer_client
from document_models import KeyValueResponse, KeyValuePair


def extract_key_values(image_path: str) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Azure Form Recognizer."""
    client = get_azure_form_recognizer_client()

    with open(image_path, "rb") as image_file:
        poller = client.begin_analyze_document("prebuilt-document", image_file)

    result = poller.result()
    key_value_pairs = []

    for kv_pair in result.key_value_pairs:
        key = kv_pair.key.content if kv_pair.key else ""
        value = kv_pair.value.content if kv_pair.value else ""

        key_bbox = {
            "vertices": [
                {"x": point.x, "y": point.y}
                for point in kv_pair.key.bounding_regions[0].polygon
            ]
            if kv_pair.key and kv_pair.key.bounding_regions
            else []
        }

        value_bbox = {
            "vertices": [
                {"x": point.x, "y": point.y}
                for point in kv_pair.value.bounding_regions[0].polygon
            ]
            if kv_pair.value and kv_pair.value.bounding_regions
            else []
        }

        key_value_pairs.append(
            KeyValuePair(
                key=key,
                value=value,
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
            )
        )

    return KeyValueResponse(
        provider="azure_form_recognizer", key_value_pairs=key_value_pairs
    )
