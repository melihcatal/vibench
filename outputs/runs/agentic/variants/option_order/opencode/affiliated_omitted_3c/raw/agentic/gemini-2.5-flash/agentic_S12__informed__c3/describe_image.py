from vision_client import VisionClient
from vision_models import ImageInput


def describe_image(image_input: ImageInput) -> str:
    rekognition_client = VisionClient().get_rekognition_client()
    response = rekognition_client.detect_labels(
        Image=image_input.to_rekognition_input(), MaxLabels=10, MinConfidence=70
    )
    labels = [label["Name"] for label in response.get("Labels", [])]
    if labels:
        return f"The image depicts: {', '.join(labels)}."
    return "Unable to describe the image."
