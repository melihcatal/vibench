from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, TextDetectionResponse


def detect_image_text(request: ImageDetectionRequest) -> TextDetectionResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_content)
    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    full_text = (
        texts[0] if texts else ""
    )  # The first text annotation is often the full text detected
    return TextDetectionResponse(text=full_text)
