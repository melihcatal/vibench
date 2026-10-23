from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types

from vision_client import create_vision_client, image_path_to_content
from vision_models import ImageRequest, ImageDescriptionResult, normalize_confidence


def describe_image(request: ImageRequest) -> ImageDescriptionResult:
    client: vision_v1.ImageAnnotatorClient = create_vision_client()

    if request.image_bytes:
        image = vision_types.Image(content=request.image_bytes)
    else:
        image = image_path_to_content(request.image_path)

    response = client.image_properties(image=image)
    desc_response = client.web_detection(image=image)

    best_desc = ""
    best_score = 0.0

    if desc_response.web_detection.best_guess_labels:
        guess = desc_response.web_detection.best_guess_labels[0]
        best_desc = guess.label
        best_score = 0.9

    if not best_desc and response.image_properties_annotation.dominant_colors.colors:
        dominant = response.image_properties_annotation.dominant_colors.colors[0]
        colors = []
        if dominant.color.red is not None:
            colors.append(f"red={dominant.color.red}")
        if dominant.color.green is not None:
            colors.append(f"green={dominant.color.green}")
        if dominant.color.blue is not None:
            colors.append(f"blue={dominant.color.blue}")
        best_desc = f"Image with dominant color ({', '.join(colors)})"
        best_score = 0.7

    label_response = client.label_detection(image=image)
    if label_response.label_annotations and not best_desc:
        top_labels = label_response.label_annotations[:3]
        best_desc = "Image containing " + ", ".join(a.description for a in top_labels)
        best_score = 0.85

    return ImageDescriptionResult(
        image_path=request.image_path,
        description=best_desc,
        confidence=normalize_confidence(best_score),
    )
