"""
[SAME-SCENARIO] Extracts key-value pairs from a form-like document.

Provider: Google Document AI (google-cloud-documentai)
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model/Processor: Form Parser processor (projects/{project}/locations/{location}/processors/{processor_id})
Service endpoint: documentai.googleapis.com
"""

from __future__ import annotations

import os
from typing import Optional, List, Dict, Any

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document as documentai_types

from document_client import load_image_bytes, get_google_project_id
from document_models import (
    KeyValueEntry,
    BoundingBox,
    OcrDocumentResult,
)


def extract_key_values_from_document(
    file_path: str,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> OcrDocumentResult:
    """
    Extract key-value pairs from a form-like document using
    Google Document AI Form Parser (documentai.googleapis.com).

    Returns an OcrDocumentResult with populated key_value_pairs list.
    """
    project_id = project_id or get_google_project_id()
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable or project_id argument is required"
        )

    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client_options = ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    raw_bytes = load_image_bytes(file_path)
    if mime_type is None:
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "application/pdf" if ext == ".pdf" else "image/png"

    raw_document = documentai.RawDocument(
        content=raw_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document
    full_text = document.text

    key_value_pairs: List[KeyValueEntry] = []
    page_count = len(document.pages)

    for page in document.pages:
        page_kvs = _extract_page_key_values(page, full_text)
        key_value_pairs.extend(page_kvs)

    return OcrDocumentResult(
        plain_text=full_text,
        key_value_pairs=key_value_pairs,
        page_count=page_count,
    )


def _extract_page_key_values(
    page: documentai_types.Document.Page,
    full_text: str,
) -> List[KeyValueEntry]:
    """Extract key-value pairs from form fields on a page."""
    entries: List[KeyValueEntry] = []

    for field in page.form_fields:
        key_text = ""
        value_text = ""
        key_bbox: Optional[BoundingBox] = None
        value_bbox: Optional[BoundingBox] = None

        # Extract field name (key)
        if field.field_name and field.field_name.text_anchor:
            key_text = _text_from_text_anchor(field.field_name.text_anchor, full_text)
        if field.field_name and field.field_name.layout:
            key_bbox = _bbox_from_layout(field.field_name.layout)

        # Extract field value
        if field.field_value and field.field_value.text_anchor:
            value_text = _text_from_text_anchor(field.field_value.text_anchor, full_text)
        if field.field_value and field.field_value.layout:
            value_bbox = _bbox_from_layout(field.field_value.layout)

        # Handle nested value (e.g., checkbox, composite values)
        if field.field_value and field.field_value.text_segments:
            if not value_text:
                parts = []
                for seg in field.field_value.text_segments:
                    start = int(seg.start_index)
                    end = int(seg.end_index)
                    parts.append(full_text[start:end])
                value_text = "".join(parts).strip()

        confidence = 1.0
        if field.field_name and hasattr(field.field_name, "confidence"):
            confidence = getattr(field.field_name, "confidence", 1.0)

        entries.append(
            KeyValueEntry(
                key=key_text,
                value=value_text,
                confidence=confidence,
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
            )
        )

    return entries


def _text_from_text_anchor(
    text_anchor: Any,
    full_text: str,
) -> str:
    """Extract text from a Document AI text_anchor using segment offsets."""
    if text_anchor and text_anchor.text_segments:
        start = int(text_anchor.text_segments[0].start_index)
        end = int(text_anchor.text_segments[-1].end_index)
        return full_text[start:end].strip()
    return ""


def _bbox_from_layout(layout: Any) -> Optional[BoundingBox]:
    """Build a BoundingBox from a layout element's normalized vertices."""
    if layout and layout.bounding_poly:
        vertices = layout.bounding_poly.normalized_vertices
        if vertices:
            return BoundingBox.from_docai_vertices(
                [{"x": v.x, "y": v.y} for v in vertices]
            )
    return None
