import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageRequest, TextDetectionResult, VisionResponse


def detect_image_text(request: ImageRequest) -> VisionResponse:
    client = get_vision_client()
    image = vision_v1.Image()

    if request.image_content:
        image.content = request.image_content
    elif request.image_uri:
        image.source.image_uri = request.image_uri
    else:
        raise ValueError("Image content or image URI must be provided.")

    response = client.text_detection(image=image)

    text_annotations = []
    if response.text_annotations:
        # The first annotation is the full text, subsequent ones are individual words/lines.
        # We'll return the full text and individual annotations with bounds.
        full_text = response.text_annotations[0].description
        for annotation in response.text_annotations[
            1:
        ]:  # Skip the first one as it's full text
            bounds = []
            for vertex in annotation.bounding_poly.vertices:
                bounds.extend([vertex.x, vertex.y])
            text_annotations.append(
                TextDetectionResult(text=annotation.description, bounds=bounds)
            )
    else:
        full_text = ""

    return VisionResponse(
        text_annotations=text_annotations, full_text_annotation=full_text
    )
