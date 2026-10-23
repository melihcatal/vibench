from vision_client import VisionClient, ImageRequest
from vision_models import TextDetectionResponse
from google.cloud import vision


def detect_image_text(image_request: ImageRequest) -> TextDetectionResponse:
    client = VisionClient()
    image = client.get_image_source(image_request)

    if isinstance(image, vision.ImageSource):
        response = client.get_client().text_detection(image=vision.Image(source=image))
    else:
        response = client.get_client().text_detection(image=image)

    text_annotations = []
    if response.text_annotations:
        for text in response.text_annotations:
            text_annotations.append(
                {
                    "description": text.description,
                    "bounding_poly": [
                        {"x": v.x, "y": v.y} for v in text.bounding_poly.vertices
                    ],
                }
            )

    return TextDetectionResponse(text_annotations=text_annotations)
