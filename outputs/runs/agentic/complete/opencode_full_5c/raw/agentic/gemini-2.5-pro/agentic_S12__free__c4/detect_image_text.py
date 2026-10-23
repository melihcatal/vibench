from google.cloud import vision
from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse, ImageText


def detect_text(request: VisionRequest) -> VisionResponse:
    """Detects text in the image."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    texts = []
    for text in response.text_annotations:
        vertices = [[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices]
        texts.append(ImageText(text=text.description, bounding_box=vertices))

    return VisionResponse(texts=texts)
