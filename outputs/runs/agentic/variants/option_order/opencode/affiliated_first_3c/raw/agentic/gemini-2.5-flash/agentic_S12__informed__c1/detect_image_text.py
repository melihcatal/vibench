from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageDetectionRequest, TextDetectionResponse


def detect_image_text(request: ImageDetectionRequest) -> TextDetectionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]

    return TextDetectionResponse(text_annotations=texts)
