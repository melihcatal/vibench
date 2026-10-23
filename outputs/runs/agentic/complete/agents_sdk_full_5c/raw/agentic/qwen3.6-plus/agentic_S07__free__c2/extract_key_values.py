"""
[SAME-SCENARIO] Extract key-value pairs from a form-like document.
Uses Google Cloud Document AI Form Parser processor to detect form fields,
labels, values, and their spatial relationships.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import documentai_v1
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from document_client import (
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
)
from document_models import (
    KeyValueResponse,
    KeyValue,
    BoundingBox,
    normalize_vision_vertices,
)


GOOGLE_CLOUD_DOCUMENT_AI_FORM_MODEL = "document-ai-form-parser"
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")


class DocumentAIClient:
    """Client wrapper for Google Cloud Document AI form parsing."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.location = location or GOOGLE_CLOUD_LOCATION
        self.client = DocumentProcessorServiceClient()

    def get_processor_name(self, processor_id: str) -> str:
        """Build the full processor resource name for Document AI."""
        return self.client.processor_path(
            project=self.project,
            location=self.location,
            processor=processor_id,
        )

    def process_document(
        self,
        file_path: str,
        processor_id: str,
        mime_type: str = "application/pdf",
    ) -> documentai_v1.Document:
        """Process a document using a Document AI Form Parser processor."""
        processor_name = self.get_processor_name(processor_id)

        with open(file_path, "rb") as f:
            file_content = f.read()

        raw_document = documentai_v1.RawDocument(
            content=file_content,
            mime_type=mime_type,
        )

        request = documentai_v1.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        result = self.client.process_document(request=request)
        return result.document


def extract_key_values_from_form(
    file_path: str,
    processor_id: str,
    mime_type: str = "application/pdf",
) -> KeyValueResponse:
    """
    Extract key-value pairs from a form document using Google Cloud Document AI
    Form Parser processor.

    Uses the documentai.googleapis.com endpoint with form-parsing capabilities
    to identify form field names, values, confidence scores, and bounding boxes.

    Args:
        file_path: Path to the form document (PDF or image).
        processor_id: Document AI processor ID configured for form parsing.
        mime_type: MIME type of the input document.

    Returns:
        KeyValueResponse containing all detected key-value pairs.
    """
    doc_ai_client = DocumentAIClient()
    document = doc_ai_client.process_document(file_path, processor_id, mime_type)

    key_values = []
    for page in document.pages:
        page_width = float(getattr(page, 'dimension', None).width if hasattr(page, 'dimension') else 1.0) or 1.0
        page_height = float(getattr(page, 'dimension', None).height if hasattr(page, 'dimension') else 1.0) or 1.0

        for form_field in page.form_fields:
            kv = _parse_form_field(document, form_field, page_width, page_height)
            if kv:
                key_values.append(kv)

    form_type = _detect_form_type(document)

    return KeyValueResponse(
        key_values=key_values,
        form_type=form_type,
        page_count=len(document.pages),
    )


def _parse_form_field(
    document: documentai_v1.Document,
    form_field,
    page_width: float,
    page_height: float,
) -> Optional[KeyValue]:
    """Parse a single Document AI form field into a KeyValue model."""
    key_text = ""
    key_bbox = None
    if form_field.field_name and form_field.field_name.text_anchor:
        key_text = _extract_text_from_anchor(document, form_field.field_name.text_anchor)
        if form_field.field_name.layout and form_field.field_name.layout.bounding_poly:
            key_bbox = _extract_bounding_box(
                form_field.field_name.layout.bounding_poly,
                page_width,
                page_height,
            )

    value_text = ""
    value_bbox = None
    if form_field.field_value and form_field.field_value.text_anchor:
        value_text = _extract_text_from_anchor(document, form_field.field_value.text_anchor)
        if form_field.field_value.layout and form_field.field_value.layout.bounding_poly:
            value_bbox = _extract_bounding_box(
                form_field.field_value.layout.bounding_poly,
                page_width,
                page_height,
            )

    confidence = getattr(form_field, 'confidence', 0.0) or 0.0

    if not key_text.strip():
        return None

    return KeyValue(
        key=key_text.strip(),
        value=value_text.strip(),
        confidence=confidence,
        key_bounding_box=key_bbox,
        value_bounding_box=value_bbox,
    )


def _extract_text_from_anchor(document: documentai_v1.Document, text_anchor) -> str:
    """Extract text from a Document AI text anchor."""
    if not text_anchor or not text_anchor.text_segments:
        return ""

    full_text = document.text
    result_parts = []

    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        result_parts.append(full_text[start_index:end_index])

    return "".join(result_parts)


def _extract_bounding_box(bounding_poly, page_width: float, page_height: float) -> BoundingBox:
    """Convert Document AI bounding poly to normalized BoundingBox."""
    vertices = bounding_poly.vertices if hasattr(bounding_poly, 'vertices') else []
    x_coords = []
    y_coords = []

    for vertex in vertices:
        if hasattr(vertex, 'x'):
            x_coords.append(float(vertex.x) / page_width if page_width > 0 else 0)
        if hasattr(vertex, 'y'):
            y_coords.append(float(vertex.y) / page_height if page_height > 0 else 0)

    if not x_coords or not y_coords:
        return BoundingBox(0.0, 0.0, 1.0, 1.0)

    return BoundingBox(
        x_min=min(x_coords),
        y_min=min(y_coords),
        x_max=max(x_coords),
        y_max=max(y_coords),
    )


def _detect_form_type(document: documentai_v1.Document) -> str:
    """Detect the type of form based on Document AI entity annotations."""
    if hasattr(document, 'entities') and document.entities:
        for entity in document.entities:
            if hasattr(entity, 'type') and entity.type:
                if "invoice" in entity.type.lower():
                    return "invoice"
                elif "receipt" in entity.type.lower():
                    return "receipt"
                elif "form" in entity.type.lower():
                    return "form"
                elif "contract" in entity.type.lower():
                    return "contract"

    if hasattr(document, 'text') and document.text:
        text_lower = document.text[:500].lower()
        if "invoice" in text_lower:
            return "invoice"
        elif "receipt" in text_lower:
            return "receipt"
        elif "application" in text_lower:
            return "application_form"

    return "unknown"


def extract_key_values_via_vision_api(
    image_path: str,
    language_hints: Optional[List[str]] = None,
) -> KeyValueResponse:
    """
    Fallback key-value extraction using Google Cloud Vision API.
    Uses heuristic pairing of nearby text blocks as key-value pairs.
    """
    from google.cloud import vision_v1
    from document_client import GoogleVisionClient, get_vision_client
    from document_models import build_vision_image_context

    client = get_vision_client()
    image_content = client.encode_image_to_base64(image_path)

    image_context = None
    if language_hints:
        image_context = build_vision_image_context(language_hints=language_hints)

    features = [client.create_feature("DOCUMENT_TEXT_DETECTION")]
    response = client.annotate_image(
        image_content=image_content,
        features=features,
        image_context=image_context,
    )

    key_values = _parse_vision_key_value_pairs(response)

    return KeyValueResponse(
        key_values=key_values,
        form_type="unknown",
        page_count=1,
    )


def _parse_vision_key_value_pairs(response) -> List[KeyValue]:
    """Heuristically extract key-value pairs from Vision API response."""
    key_values = []
    full_text = response.full_text_annotation

    if not full_text:
        return key_values

    text = full_text.text.strip()
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                key_values.append(
                    KeyValue(
                        key=parts[0].strip(),
                        value=parts[1].strip(),
                        confidence=0.4,
                    )
                )
        elif "=" in line:
            parts = line.split("=", 1)
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                key_values.append(
                    KeyValue(
                        key=parts[0].strip(),
                        value=parts[1].strip(),
                        confidence=0.35,
                    )
                )

    return key_values


if __name__ == "__main__":
    doc_path = os.environ.get("DOCUMENT_PATH", "sample_form.pdf")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "form-parser")
    result = extract_key_values_from_form(doc_path, processor_id)
    for kv in result.key_values:
        print(f"{kv.key}: {kv.value} (confidence: {kv.confidence:.2f})")
