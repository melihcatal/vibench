from vision_client import VisionClient
from vision_models import ImageInput, ImageSafetyResponse, SafetyAnnotation
from google.cloud import vision_v1p3beta1 as vision # Ensure this import matches vision_client

def score_image_safety(image_input: ImageInput) -> ImageSafetyResponse:
    client = VisionClient()
    google_vision_client = client.get_google_vision_client()

    image = vision.Image()
    if image_input.image_url:
        image.source.image_uri = image_input.image_url
    elif image_input.image_base64:
        image.content = image_input.image_base64
    else:
        raise ValueError("Either image_url or image_base64 must be provided.")

    response = google_vision_client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    annotations = []
    # The likelihood values are numbers, which map to specific strings.
    # Let's define a helper to convert them.
    likelihood_map = {
        vision.Likelihood.UNKNOWN: 'UNKNOWN',
        vision.Likelihood.VERY_UNLIKELY: 'VERY_UNLIKELY',
        vision.Likelihood.UNLIKELY: 'UNLIKELY',
        vision.Likelihood.POSSIBLE: 'POSSIBLE',
        vision.Likelihood.LIKELY: 'LIKELY',
        vision.Likelihood.VERY_LIKELY: 'VERY_LIKELY',
    }

    annotations.append(SafetyAnnotation(category="adult", likelihood=likelihood_map[safe_search_annotation.adult]))
    annotations.append(SafetyAnnotation(category="spoof", likelihood=likelihood_map[safe_search_annotation.spoof]))
    annotations.append(SafetyAnnotation(category="medical", likelihood=likelihood_map[safe_search_annotation.medical]))
    annotations.append(SafetyAnnotation(category="violence", likelihood=likelihood_map[safe_search_annotation.violence]))
    annotations.append(SafetyAnnotation(category="racy", likelihood=likelihood_map[safe_search_annotation.racy]))

    return ImageSafetyResponse(annotations=annotations)