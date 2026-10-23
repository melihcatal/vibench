"""
extract_key_values.py - Extracts key-value pairs from a form-like document
using Azure Document Intelligence (prebuilt-document / general document model).

Provider: Azure AI Document Intelligence
Model: prebuilt-document (general document model for key-value extraction)
"""

from typing import Optional, Dict, Any, Union

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer._models import AnalyzeResult, DocumentField
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from document_client import (
    DocumentClientConfig,
    get_azure_doc_intelligence_client,
    normalize_image_to_bytes,
)
from document_models import (
    KeyValueResult,
    KeyValueEntry,
    BoundingBox,
    normalize_azure_kv_to_entries,
)


def extract_key_values_from_document(
    document_data: Union[str, bytes, Any],
    client: Optional[DocumentAnalysisClient] = None,
) -> KeyValueResult:
    """
    Extract key-value pairs from a form-like document using
    Azure Document Intelligence's general document model.

    Args:
        document_data: Document as bytes, file path string, or file-like object.
        client: Optional pre-configured DocumentAnalysisClient instance.

    Returns:
        KeyValueResult containing extracted key-value pairs.
    """
    if client is None:
        client = get_azure_doc_intelligence_client()

    doc_bytes = normalize_image_to_bytes(document_data)

    try:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            document=doc_bytes,
        )
        result: AnalyzeResult = poller.result()
    except HttpResponseError as e:
        raise RuntimeError(f"Azure Document Intelligence key-value extraction failed: {e}") from e

    return _parse_azure_kv_result(result)


def _parse_azure_kv_result(result: AnalyzeResult) -> KeyValueResult:
    """Parse Azure Document Intelligence AnalyzeResult into KeyValueResult."""
    all_entries = []

    # Extract key-value pairs from documents
    for doc in result.documents:
        fields = doc.fields if hasattr(doc, "fields") and doc.fields else {}
        entries = _extract_fields_as_kv(fields)
        all_entries.extend(entries)

    # Also check for key-value pairs detected at the page level
    if hasattr(result, "key_value_pairs") and result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_content = ""
            value_content = ""
            key_confidence = 0.0

            if hasattr(kv_pair, "key") and kv_pair.key:
                key_content = kv_pair.key.content if hasattr(kv_pair.key, "content") else ""
                key_confidence = kv_pair.key.confidence if hasattr(kv_pair.key, "confidence") else 0.0

            if hasattr(kv_pair, "value") and kv_pair.value:
                value_content = kv_pair.value.content if hasattr(kv_pair.value, "content") else ""

            bbox = None
            if hasattr(kv_pair, "key") and kv_pair.key:
                if hasattr(kv_pair.key, "bounding_regions") and kv_pair.key.bounding_regions:
                    region = kv_pair.key.bounding_regions[0]
                    polygon = list(region.polygon) if hasattr(region, "polygon") and region.polygon else []
                    if len(polygon) >= 8:
                        bbox = BoundingBox.from_polygon(polygon).to_dict()

            all_entries.append(KeyValueEntry(
                key=key_content,
                value=value_content,
                confidence=key_confidence,
                bounding_box=bbox,
            ))

    model_id = result.model_id if hasattr(result, "model_id") else "prebuilt-document"

    return KeyValueResult(
        key_value_pairs=all_entries,
        model_id=model_id,
    )


def _extract_fields_as_kv(
    fields: Dict[str, DocumentField],
    prefix: str = "",
) -> list:
    """Recursively extract key-value pairs from Azure DocumentField objects."""
    entries = []

    for field_name, field_value in fields.items():
        full_key = f"{prefix}/{field_name}" if prefix else field_name

        if field_value is None:
            continue

        field_type = field_value.type if hasattr(field_value, "type") else "string"

        if field_type == "object" and hasattr(field_value, "value") and isinstance(field_value.value, dict):
            # Recurse into nested objects
            nested_entries = _extract_fields_as_kv(field_value.value, prefix=full_key)
            entries.extend(nested_entries)
        elif field_type == "array" and hasattr(field_value, "value") and isinstance(field_value.value, list):
            # Handle array-type fields
            for idx, item in enumerate(field_value.value):
                if isinstance(item, DocumentField):
                    nested_key = f"{full_key}[{idx}]"
                    if hasattr(item, "value") and isinstance(item.value, dict):
                        nested_entries = _extract_fields_as_kv(item.value, prefix=nested_key)
                        entries.extend(nested_entries)
                    else:
                        entries.append(KeyValueEntry(
                            key=nested_key,
                            value=str(item.value) if item.value is not None else "",
                            confidence=item.confidence if hasattr(item, "confidence") else 0.0,
                        ))
                else:
                    entries.append(KeyValueEntry(
                        key=f"{full_key}[{idx}]",
                        value=str(item) if item is not None else "",
                        confidence=field_value.confidence if hasattr(field_value, "confidence") else 0.0,
                    ))
        else:
            value = field_value.value if hasattr(field_value, "value") else ""
            confidence = field_value.confidence if hasattr(field_value, "confidence") else 0.0

            bbox = None
            if hasattr(field_value, "bounding_regions") and field_value.bounding_regions:
                region = field_value.bounding_regions[0]
                polygon = list(region.polygon) if hasattr(region, "polygon") and region.polygon else []
                if len(polygon) >= 8:
                    bbox = BoundingBox.from_polygon(polygon).to_dict()

            entries.append(KeyValueEntry(
                key=full_key,
                value=str(value) if value is not None else "",
                confidence=confidence,
                bounding_box=bbox,
            ))

    return entries


def extract_key_values_from_url(
    document_url: str,
    client: Optional[DocumentAnalysisClient] = None,
) -> KeyValueResult:
    """
    Extract key-value pairs from a document accessible via URL.

    Args:
        document_url: Public URL of the document.
        client: Optional pre-configured DocumentAnalysisClient instance.

    Returns:
        KeyValueResult with extracted key-value pairs.
    """
    if client is None:
        client = get_azure_doc_intelligence_client()

    try:
        poller = client.begin_analyze_document_from_url(
            "prebuilt-document",
            document_url=document_url,
        )
        result: AnalyzeResult = poller.result()
    except HttpResponseError as e:
        raise RuntimeError(f"Azure Document Intelligence URL KV extraction failed: {e}") from e

    return _parse_azure_kv_result(result)


def get_field_value(
    result: KeyValueResult,
    field_name: str,
    default: str = "",
) -> str:
    """
    Retrieve a specific field value from the extraction result.

    Args:
        result: KeyValueResult from extraction.
        field_name: The key to look up.
        default: Default value if key is not found.

    Returns:
        The value associated with the key, or the default.
    """
    for entry in result.key_value_pairs:
        if entry.key == field_name or field_name in entry.key:
            return entry.value
    return default
