from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageDetectionRequest, LabelDetectionResponse


def detect_image_labels(request: ImageDetectionRequest) -> LabelDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    return LabelDetectionResponse(labels=labels)
