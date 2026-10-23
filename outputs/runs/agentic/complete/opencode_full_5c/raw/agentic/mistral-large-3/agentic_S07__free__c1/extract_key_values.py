from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import KeyValueResponse, KeyValuePair


def extract_key_values(image_path: str) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    key_value_pairs = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (
                            symbol.property.detected_break.type_
                            == types.TextAnnotation.DetectedBreak.BreakType.EQUALS_SIGN
                        ):
                            key = "".join(
                                [
                                    s.text
                                    for s in word.symbols[: word.symbols.index(symbol)]
                                ]
                            )
                            value = "".join(
                                [
                                    s.text
                                    for s in word.symbols[
                                        word.symbols.index(symbol) + 1 :
                                    ]
                                ]
                            )
                            key_value_pairs.append(KeyValuePair(key=key, value=value))

    return KeyValueResponse(pairs=key_value_pairs)
