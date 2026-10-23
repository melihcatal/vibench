from google.cloud import documentai_v1 as documentai
import os
from typing import List, Dict, Any
from document_client import get_document_client
from document_models import LayoutElement, LayoutResponse


def extract_layout_from_image(
    image_path: str, mime_type: str = "image/png"
) -> LayoutResponse:
    """
    Extracts layout elements (blocks, lines, tables) from a document using Google Document AI.

    Args:
        image_path: Path to the document image file.
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        LayoutResponse containing layout elements and metadata.
    """
    client = get_document_client("google")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError(
            "Google Cloud project ID and processor ID must be set in environment variables."
        )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {"content": image_content, "mime_type": mime_type},
    }

    result = client.process_document(request=request)
    document = result.document

    layout_elements = []
    for page in document.pages:
        for block in page.blocks:
            layout_elements.append(
                LayoutElement(
                    element_type="block",
                    text=block.layout.text_anchor.content
                    if block.layout.text_anchor
                    else "",
                    bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in block.layout.bounding_poly.normalized_vertices
                        ]
                    },
                    confidence=block.layout.confidence,
                )
            )
        for paragraph in page.paragraphs:
            layout_elements.append(
                LayoutElement(
                    element_type="paragraph",
                    text=paragraph.layout.text_anchor.content
                    if paragraph.layout.text_anchor
                    else "",
                    bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in paragraph.layout.bounding_poly.normalized_vertices
                        ]
                    },
                    confidence=paragraph.layout.confidence,
                )
            )
        for line in page.lines:
            layout_elements.append(
                LayoutElement(
                    element_type="line",
                    text=line.layout.text_anchor.content
                    if line.layout.text_anchor
                    else "",
                    bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in line.layout.bounding_poly.normalized_vertices
                        ]
                    },
                    confidence=line.layout.confidence,
                )
            )

    return LayoutResponse(
        elements=layout_elements,
        pages=len(document.pages),
        provider="google_document_ai",
        model="pretrained-layout-v2.0-2023-06-02",
    )
