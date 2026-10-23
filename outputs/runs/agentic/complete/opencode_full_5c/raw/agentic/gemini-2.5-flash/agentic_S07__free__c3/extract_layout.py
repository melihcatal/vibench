import io
import os
from typing import Union

from google.cloud import documentai_v1 as documentai

from document_client import GoogleCloudClients
from document_models import ExtractedLayout, LayoutElement, BoundingPoly


def _convert_bounding_poly(document_proto_bounding_poly) -> BoundingPoly:
    if not document_proto_bounding_poly:
        return BoundingPoly(vertices=[])
    vertices = []
    for vertex in document_proto_bounding_poly.vertices:
        vertices.append({"x": vertex.x, "y": vertex.y})
    return BoundingPoly(vertices=vertices)


def extract_layout_from_document(
    document_bytes: bytes, mime_type: str
) -> ExtractedLayout:
    """Extracts layout elements (paragraphs, lines) from a document using Google Cloud Document AI.

    Args:
        document_bytes: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., 'application/pdf', 'image/tiff').

    Returns:
        An ExtractedLayout object containing a list of layout elements.
    """
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    location = os.environ.get("GOOGLE_LOCATION")
    # Using a general form parser processor for layout extraction
    processor_id = os.environ.get(
        "DOCUMENT_AI_PROCESSOR_ID", "YOUR_FORM_PARSER_PROCESSOR_ID"
    )  # Replace with your processor ID

    if not project_id or not location or not processor_id:
        raise ValueError(
            "GOOGLE_PROJECT_ID, GOOGLE_LOCATION, and DOCUMENT_AI_PROCESSOR_ID environment variables must be set."
        )

    client = GoogleCloudClients.get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    layout_elements: list[LayoutElement] = []

    # Extract paragraphs
    for paragraph in document.pages[0].paragraphs:
        text_content = document.text[
            paragraph.layout.text_anchor.text_segments[
                0
            ].start_index : paragraph.layout.text_anchor.text_segments[0].end_index
        ]
        layout_elements.append(
            LayoutElement(
                text_content=text_content,
                bounding_box=_convert_bounding_poly(paragraph.layout.bounding_poly),
                element_type="paragraph",
            )
        )

    # Extract lines (tokens can be grouped into lines)
    # Document AI doesn't directly give 'lines' as a top-level element in layout,
    # but tokens are usually what make up lines. For simplicity, we can treat tokens as basic layout elements or reconstruct lines.
    # For this example, let's extract tokens as a finer-grained layout element.
    for token in document.pages[0].tokens:
        text_content = document.text[
            token.layout.text_anchor.text_segments[
                0
            ].start_index : token.layout.text_anchor.text_segments[0].end_index
        ]
        layout_elements.append(
            LayoutElement(
                text_content=text_content,
                bounding_box=_convert_bounding_poly(token.layout.bounding_poly),
                element_type="token",
            )
        )

    return ExtractedLayout(layout_elements=layout_elements)
