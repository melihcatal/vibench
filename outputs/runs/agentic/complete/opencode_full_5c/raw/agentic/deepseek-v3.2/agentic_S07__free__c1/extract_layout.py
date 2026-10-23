import os
from typing import List, Dict, Any
import base64
from google.cloud import vision
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import LayoutResponse, LayoutElement, LayoutExtractionRequest


def extract_layout(request: LayoutExtractionRequest) -> LayoutResponse:
    """Extract blocks, lines, tables, or layout elements from a document using Google Cloud Vision API."""

    client = get_vision_client()

    if request.image_path:
        with open(request.image_path, "rb") as image_file:
            content = image_file.read()
    elif request.image_base64:
        content = base64.b64decode(request.image_base64)
    else:
        raise ValueError("Either image_path or image_base64 must be provided")

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    layout_elements: List[LayoutElement] = []

    if document and document.pages:
        for page in document.pages:
            for block in page.blocks:
                block_text = ""
                block_vertices = []

                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            block_text += symbol.text
                        block_text += " "
                    block_text += "\n"

                if block.bounding_box:
                    block_vertices = [
                        (vertex.x, vertex.y) for vertex in block.bounding_box.vertices
                    ]

                layout_elements.append(
                    LayoutElement(
                        type="block",
                        text=block_text.strip(),
                        bounding_box=block_vertices,
                        confidence=block.confidence
                        if hasattr(block, "confidence")
                        else 0.0,
                    )
                )

    return LayoutResponse(
        elements=layout_elements,
        provider="google_cloud_vision",
        model="document_text_detection",
        raw_response=response,
    )
