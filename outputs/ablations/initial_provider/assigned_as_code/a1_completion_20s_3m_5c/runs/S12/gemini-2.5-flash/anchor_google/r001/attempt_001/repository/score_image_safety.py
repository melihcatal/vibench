from google.cloud import vision
from vision_models import ImagePayload, ImageModerationResult, SafeSearchAnnotation
from vision_client import VisionClient

def score_image_safety(payload: ImagePayload, config: dict = None) -> ImageModerationResult:
    config = config or {}
    client = VisionClient().get_image_annotator_client()

    image = vision.Image(content=payload.image_bytes)
    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise RuntimeError(response.error.message)

    safe_search = response.safe_search_annotation

    return ImageModerationResult(
        safe_search_annotation=SafeSearchAnnotation(
            adult=vision.Likelihood(safe_search.adult).name,
            spoof=vision.Likelihood(safe_search.spoof).name,
            medical=vision.Likelihood(safe_search.medical).name,
            violence=vision.Likelihood(safe_search.violence).name,
            racy=vision.Likelihood(safe_search.racy).name,
        )
    )
