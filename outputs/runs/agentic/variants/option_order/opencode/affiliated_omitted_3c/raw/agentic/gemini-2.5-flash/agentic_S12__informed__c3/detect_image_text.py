from vision_client import VisionClient
from vision_models import ImageInput, RekognitionTextDetection


def detect_image_text(image_input: ImageInput) -> list[RekognitionTextDetection]:
    rekognition_client = VisionClient().get_rekognition_client()
    response = rekognition_client.detect_text(Image=image_input.to_rekognition_input())
    return [
        RekognitionTextDetection(text) for text in response.get("TextDetections", [])
    ]
