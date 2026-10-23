import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageRequest, SafeSearchDetectionResult, VisionResponse


def score_image_safety(request: ImageRequest) -> VisionResponse:
    client = get_vision_client()
    image = vision_v1.Image()

    if request.image_content:
        image.content = request.image_content
    elif request.image_uri:
        image.source.image_uri = request.image_uri
    else:
        raise ValueError("Image content or image URI must be provided.")

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    if safe_search:
        result = SafeSearchDetectionResult(
            adult=vision_v1.Likelihood(safe_search.adult).name,
            spoof=vision_v1.Likelihood(safe_search.spoof).name,
            medical=vision_v1.Likelihood(safe_search.medical).name,
            violence=vision_v1.Likelihood(safe_search.violence).name,
            racy=vision_v1.Likelihood(safe_search.racy).name,
        )
        return VisionResponse(safe_search_annotation=result)
    return VisionResponse()
