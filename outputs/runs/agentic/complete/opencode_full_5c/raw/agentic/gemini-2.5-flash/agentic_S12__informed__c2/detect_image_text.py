from vision_client import VisionClient
from vision_models import (
    ImageDetectionRequest,
    ImageTextDetectionResponse,
    TextAnnotation,
)
from google.cloud import vision


def detect_image_text(request: ImageDetectionRequest) -> ImageTextDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    text_annotations = []
    for text in response.text_annotations:
        bounds = [[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices]
        text_annotations.append(
            TextAnnotation(description=text.description, bounds=bounds)
        )

    return ImageTextDetectionResponse(text_annotations=text_annotations)
