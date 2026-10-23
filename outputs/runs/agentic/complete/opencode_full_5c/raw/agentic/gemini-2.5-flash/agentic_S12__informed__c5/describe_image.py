from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, ImageDescriptionResult
from google.cloud import (
    vision,
)  # Google Cloud Vision SDK import is the identifying signal


def describe_image(request: ImageAnalysisRequest) -> ImageDescriptionResult:
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    # Using web detection to get entities and form a description
    response = client.web_detection(image=image)
    description_parts = []
    if response.web_detection.best_guess_labels:
        for label in response.web_detection.best_guess_labels:
            description_parts.append(label.label)
    if response.web_detection.web_entities:
        for entity in response.web_detection.web_entities:
            if entity.description and entity.score > 0.5:
                description_parts.append(entity.description)

    description = ", ".join(list(set(description_parts[:5])))  # Limit to 5 unique parts
    if not description:
        # Fallback to label detection if web detection is sparse
        label_response = client.label_detection(image=image)
        if label_response.label_annotations:
            for label in label_response.label_annotations[:3]:  # Take top 3 labels
                description_parts.append(label.description)
            description = ", ".join(list(set(description_parts)))

    return ImageDescriptionResult(
        description=description if description else "No clear description found."
    )
