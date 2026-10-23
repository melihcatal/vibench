from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import OCRResponse


def extract_text(
    image_path: str, language_hints: Optional[List[str]] = None
) -> OCRResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = vision_v1.types.AnnotateImageRequest(
        image=image,
        features=features,
        image_context={"language_hints": language_hints} if language_hints else None,
    )

    response = client.annotate_image(request)
    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")

    full_text = response.full_text_annotation.text
    pages = []
    for page in response.full_text_annotation.pages:
        blocks = []
        for block in page.blocks:
            paragraphs = []
            for paragraph in block.paragraphs:
                words = []
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    words.append(
                        {
                            "text": word_text,
                            "confidence": word.confidence,
                            "bounding_box": {
                                "vertices": [
                                    {"x": vertex.x, "y": vertex.y}
                                    for vertex in word.bounding_box.vertices
                                ]
                            },
                        }
                    )
                paragraphs.append(
                    {
                        "text": " ".join([w["text"] for w in words]),
                        "confidence": paragraph.confidence,
                        "bounding_box": {
                            "vertices": [
                                {"x": vertex.x, "y": vertex.y}
                                for vertex in paragraph.bounding_box.vertices
                            ]
                        },
                        "words": words,
                    }
                )
            blocks.append(
                {
                    "text": "\n".join([p["text"] for p in paragraphs]),
                    "confidence": block.confidence,
                    "bounding_box": {
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in block.bounding_box.vertices
                        ]
                    },
                    "paragraphs": paragraphs,
                }
            )
        pages.append({"blocks": blocks, "width": page.width, "height": page.height})

    return OCRResponse(
        full_text=full_text,
        pages=pages,
        provider="google_vision",
        model="document_text_detection",
    )
