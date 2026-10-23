from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types

from vision_client import create_vision_client, image_path_to_content
from vision_models import ImageRequest, LabelDetectionResult, normalize_labels


def detect_image_labels(request: ImageRequest) -> LabelDetectionResult:
    client: vision_v1.ImageAnnotatorClient = create_vision_client()

    if request.image_bytes:
        image = vision_types.Image(content=request.image_bytes)
    else:
        image = image_path_to_content(request.image_path)

    response = client.label_detection(image=image)
    raw_labels = []
    for annotation in response.label_annotations:
        raw_labels.append(
            {
                "label": annotation.description,
                "confidence": annotation.score,
                "category": getattr(annotation, "category", ""),
            }
        )

    labels = normalize_labels(raw_labels)
    return LabelDetectionResult(image_path=request.image_path, labels=labels)
