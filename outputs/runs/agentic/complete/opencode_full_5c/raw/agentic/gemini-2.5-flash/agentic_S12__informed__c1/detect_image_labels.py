from vision_client import VisionClient, ImageRequest
from vision_models import LabelDetectionResponse
from google.cloud import vision


def detect_image_labels(image_request: ImageRequest) -> LabelDetectionResponse:
    client = VisionClient()
    image = client.get_image_source(image_request)

    if isinstance(image, vision.ImageSource):
        response = client.get_client().label_detection(image=vision.Image(source=image))
    else:
        response = client.get_client().label_detection(image=image)

    labels = [label.description for label in response.label_annotations]
    return LabelDetectionResponse(labels=labels)
