import google.cloud.vision as vision
from vision_client import create_vision_client
from vision_models import VisionRequest, VisionResponse


def image_summary(image_path):
    client = create_vision_client()
    request = VisionRequest(image_path)
    with open(request.image_path, "rb") as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        summary = VisionResponse(labels)
        return summary.labels
