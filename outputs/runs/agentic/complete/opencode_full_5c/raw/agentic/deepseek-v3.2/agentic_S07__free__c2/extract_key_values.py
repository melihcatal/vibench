import os
import json
from typing import Dict, List, Any, Optional
import requests


def extract_key_values_from_image(
    image_path: str, expected_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Extract key-value pairs from a form-like document using Google Document AI.

    Args:
        image_path: Path to the image file
        expected_keys: Optional list of expected key names to look for

    Returns:
        Dictionary of key-value pairs
    """
    from google.cloud import documentai

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")

    client = documentai.DocumentProcessorServiceClient()

    processor_name = client.processor_path(project_id, location, processor_id)

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = {}

    for entity in document.entities:
        if entity.type_ == "key_value_pair":
            key_text = ""
            value_text = ""

            for prop in entity.properties:
                if prop.type_ == "key":
                    key_text = prop.text_anchor.content if prop.text_anchor else ""
                elif prop.type_ == "value":
                    value_text = prop.text_anchor.content if prop.text_anchor else ""

            if key_text and value_text:
                normalized_key = (
                    key_text.strip().lower().replace(":", "").replace(" ", "_")
                )
                key_value_pairs[normalized_key] = {
                    "key": key_text.strip(),
                    "value": value_text.strip(),
                    "confidence": entity.confidence,
                }

    if expected_keys:
        filtered_pairs = {}
        for expected_key in expected_keys:
            normalized_expected = (
                expected_key.strip().lower().replace(":", "").replace(" ", "_")
            )
            for key, value in key_value_pairs.items():
                if normalized_expected in key or key in normalized_expected:
                    filtered_pairs[expected_key] = value["value"]
                    break
        return filtered_pairs

    simplified_pairs = {k: v["value"] for k, v in key_value_pairs.items()}
    return simplified_pairs


def extract_key_values_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Extract key-value pairs from a PDF document using Google Document AI.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary of key-value pairs
    """
    from google.cloud import documentai

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")

    client = documentai.DocumentProcessorServiceClient()

    processor_name = client.processor_path(project_id, location, processor_id)

    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    raw_document = documentai.RawDocument(
        content=pdf_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = {}

    for entity in document.entities:
        if entity.type_ == "key_value_pair":
            key_text = ""
            value_text = ""

            for prop in entity.properties:
                if prop.type_ == "key":
                    key_text = prop.text_anchor.content if prop.text_anchor else ""
                elif prop.type_ == "value":
                    value_text = prop.text_anchor.content if prop.text_anchor else ""

            if key_text and value_text:
                normalized_key = (
                    key_text.strip().lower().replace(":", "").replace(" ", "_")
                )
                key_value_pairs[normalized_key] = {
                    "key": key_text.strip(),
                    "value": value_text.strip(),
                    "confidence": entity.confidence,
                }

    simplified_pairs = {k: v["value"] for k, v in key_value_pairs.items()}
    return simplified_pairs
