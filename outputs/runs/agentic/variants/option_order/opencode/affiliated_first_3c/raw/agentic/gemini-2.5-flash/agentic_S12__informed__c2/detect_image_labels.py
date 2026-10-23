from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, LabelDetectionResponse


def detect_image_labels(request: ImageDetectionRequest) -> LabelDetectionResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return LabelDetectionResponse(labels=labels)
