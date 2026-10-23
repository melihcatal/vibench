from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, TextAnnotation


def detect_image_text(request: ImageAnalysisRequest) -> list[TextAnnotation]:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    text_annotations = []
    if response.text_annotations:
        # The first annotation is the overall text detected in the image
        full_text = response.text_annotations[0].description
        # Other annotations are for individual words or lines
        for text in response.text_annotations[1:]:
            bounds = [
                {"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices
            ]
            text_annotations.append(
                TextAnnotation(text=text.description, bounds=bounds)
            )
    return text_annotations
