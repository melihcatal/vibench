"""
extract_key_values.py - Extracts key-value pairs from a form-like document
using Azure AI Document Intelligence (prebuilt-document model).

Provider: Azure AI Document Intelligence
SDK: azure-ai-formrecognizer
Model: prebuilt-document
"""

from typing import List, Optional

from document_client import get_azure_client
from document_models import (
    BoundingBox,
    ExtractKeyValuesRequest,
    ExtractKeyValuesResponse,
    KeyValueEntry,
)

PROVIDER = "azure"
AZURE_MODEL_ID = "prebuilt-document"


def _extract_bbox(field) -> Optional[BoundingBox]:
    """Extract bounding box from a field's bounding regions."""
    if hasattr(field, "bounding_regions") and field.bounding_regions:
        region = field.bounding_regions[0]
        if hasattr(region, "bounding_box") and region.bounding_box:
            bb = region.bounding_box
            return BoundingBox(
                x=bb[0] if len(bb) > 0 else 0.0,
                y=bb[1] if len(bb) > 1 else 0.0,
                width=(bb[2] - bb[0]) if len(bb) > 2 else 0.0,
                height=(bb[3] - bb[1]) if len(bb) > 3 else 0.0,
            )
    return None


def _safe_value(field) -> str:
    """Safely extract a string value from a DocumentField."""
    if field is None:
        return ""
    if hasattr(field, "value"):
        val = field.value
        if val is None:
            return ""
        return str(val)
    if hasattr(field, "content"):
        return str(field.content)
    return ""


def _safe_confidence(field) -> float:
    """Safely extract confidence from a field."""
    if field is None:
        return 0.0
    return getattr(field, "confidence", 0.0)


def extract_key_values(request: ExtractKeyValuesRequest) -> ExtractKeyValuesResponse:
    """
    Extract key-value pairs from a form-like document using Azure AI
    Document Intelligence's prebuilt-document model which supports
    key-value pair extraction.

    Args:
        request: ExtractKeyValuesRequest with image source.

    Returns:
        ExtractKeyValuesResponse containing key-value entries.
    """
    from io import BytesIO
    import base64

    if request.image.base64_data is None:
        raise ValueError("Image base64_data is required for key-value extraction.")

    image_bytes = BytesIO(base64.b64decode(request.image.base64_data))

    client = get_azure_client()
    analysis_client = client.create_document_analysis_client()

    poller = analysis_client.begin_analyze_document(
        model_id=AZURE_MODEL_ID,
        document=image_bytes,
    )
    result = poller.result()

    key_values: List[KeyValueEntry] = []
    total_confidence = 0.0
    count = 0

    if hasattr(result, "key_value_pairs") and result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_field = kv_pair.key if hasattr(kv_pair, "key") else None
            value_field = kv_pair.value if hasattr(kv_pair, "value") else None

            key_text = _safe_value(key_field)
            value_text = _safe_value(value_field)

            if not key_text and not value_text:
                continue

            entry = KeyValueEntry(
                key=key_text,
                value=value_text,
                key_confidence=_safe_confidence(key_field),
                value_confidence=_safe_confidence(value_field),
                key_bounding_box=_extract_bbox(key_field),
                value_bounding_box=_extract_bbox(value_field),
            )
            key_values.append(entry)
            avg_conf = (entry.key_confidence + entry.value_confidence) / 2.0
            total_confidence += avg_conf
            count += 1

    overall_confidence = total_confidence / count if count > 0 else 0.0

    return ExtractKeyValuesResponse(
        key_values=key_values,
        confidence=overall_confidence,
        provider=PROVIDER,
        raw_response={"status": "success", "model_id": AZURE_MODEL_ID},
    )


def extract_key_values_from_file(
    file_path: str,
    form_type: str = "generic",
) -> ExtractKeyValuesResponse:
    """
    Convenience function to extract key-value pairs directly from a file path.

    Args:
        file_path: Path to the document image file.
        form_type: Optional form type hint.

    Returns:
        ExtractKeyValuesResponse with extracted key-value pairs.
    """
    from document_client import prepare_image_source

    image_source = prepare_image_source(file_path=file_path)
    req = ExtractKeyValuesRequest(
        image=image_source,
        form_type=form_type,
    )
    return extract_key_values(req)


def extract_key_values_as_dict(
    request: ExtractKeyValuesRequest,
) -> dict:
    """
    Extract key-value pairs and return them as a simple dictionary.

    Args:
        request: ExtractKeyValuesRequest with image source.

    Returns:
        Dictionary mapping keys to values.
    """
    response = extract_key_values(request)
    return {kv.key: kv.value for kv in response.key_values if kv.key}
