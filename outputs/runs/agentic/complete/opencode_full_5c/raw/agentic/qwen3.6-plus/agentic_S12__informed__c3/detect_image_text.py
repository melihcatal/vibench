from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types

from vision_client import create_vision_client, image_path_to_content
from vision_models import (
    ImageRequest,
    TextAnnotation,
    TextDetectionResult,
    build_full_text,
    normalize_confidence,
)


def detect_image_text(request: ImageRequest) -> TextDetectionResult:
    client: vision_v1.ImageAnnotatorClient = create_vision_client()

    if request.image_bytes:
        image = vision_types.Image(content=request.image_bytes)
    else:
        image = image_path_to_content(request.image_path)

    response = client.text_detection(image=image)
    annotations = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = "".join(symbol.text for symbol in word.symbols)
                    confidence = normalize_confidence(word.confidence)
                    annotations.append(
                        TextAnnotation(text=word_text, confidence=confidence)
                    )

    full_text = build_full_text(annotations)

    return TextDetectionResult(
        image_path=request.image_path,
        annotations=annotations,
        full_text=full_text,
    )
