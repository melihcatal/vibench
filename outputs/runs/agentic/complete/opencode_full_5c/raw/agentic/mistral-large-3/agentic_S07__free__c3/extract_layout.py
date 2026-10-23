from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import LayoutResponse


def extract_layout(image_path: str) -> LayoutResponse:
    """Extract layout elements (blocks, lines, tables) from a document using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = vision_v1.types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")

    layout_elements = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_vertices = [
                {"x": vertex.x, "y": vertex.y} for vertex in block.bounding_box.vertices
            ]
            block_element = {
                "type": "block",
                "text": "\n".join(
                    [
                        " ".join([symbol.text for symbol in word.symbols])
                        for paragraph in block.paragraphs
                        for word in paragraph.words
                    ]
                ),
                "bounding_box": {"vertices": block_vertices},
                "confidence": block.confidence,
                "children": [],
            }

            for paragraph in block.paragraphs:
                paragraph_vertices = [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in paragraph.bounding_box.vertices
                ]
                paragraph_element = {
                    "type": "paragraph",
                    "text": " ".join(
                        [
                            symbol.text
                            for word in paragraph.words
                            for symbol in word.symbols
                        ]
                    ),
                    "bounding_box": {"vertices": paragraph_vertices},
                    "confidence": paragraph.confidence,
                    "children": [],
                }

                for word in paragraph.words:
                    word_vertices = [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in word.bounding_box.vertices
                    ]
                    word_element = {
                        "type": "word",
                        "text": "".join([symbol.text for symbol in word.symbols]),
                        "bounding_box": {"vertices": word_vertices},
                        "confidence": word.confidence,
                        "children": [],
                    }
                    paragraph_element["children"].append(word_element)

                block_element["children"].append(paragraph_element)

            layout_elements.append(block_element)

    return LayoutResponse(
        layout_elements=layout_elements,
        provider="google_vision",
        model="document_text_detection",
    )
