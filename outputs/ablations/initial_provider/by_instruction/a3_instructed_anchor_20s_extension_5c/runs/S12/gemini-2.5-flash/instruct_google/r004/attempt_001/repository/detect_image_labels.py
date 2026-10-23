from vision_client import get_vision_client
from vision_models import ImageLabelsRequest, ImageLabel, ImageLabelsResponse
from google.cloud import vision

def detect_image_labels(image_content: bytes) -> ImageLabelsResponse:
    client = get_vision_client()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append(ImageLabel(description=label.description, score=label.score))

    return ImageLabelsResponse(labels=labels)
