from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, ImageDescriptionResponse

def describe_image(payload: ImageDetectionRequest, config: dict = None) -> ImageDescriptionResponse:
    client = get_vision_client()
    image = vision.Image(content=payload.image_bytes) if payload.image_bytes else vision.Image(image_uri=payload.image_uri)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        # Simple approach: concatenate top labels as a description
        description = ", ".join([label.description for label in labels[:int(config.get('max_labels', 5))]])
    else:
        description = "No clear description found."

    return ImageDescriptionResponse(description=description)
