from vision_client import VisionClient
from vision_models import ImageDetectionRequest, ImageLabelDetectionResponse, Label
from google.cloud import vision


def detect_image_labels(request: ImageDetectionRequest) -> ImageLabelDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    labels = [
        Label(description=label.description, score=label.score)
        for label in response.label_annotations
    ]

    return ImageLabelDetectionResponse(labels=labels)
