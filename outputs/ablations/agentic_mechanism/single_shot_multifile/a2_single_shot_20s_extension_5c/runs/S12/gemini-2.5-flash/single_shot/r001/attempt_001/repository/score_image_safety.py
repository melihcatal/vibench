import os
from google.cloud import vision_v1
from vision_client import get_vision_client, create_vision_image_object
from vision_models import ImageData, SafeSearchResult

def score_image_safety(image_data: ImageData) -> SafeSearchResult:
    """
    Checks an image for unsafe or policy-sensitive visual content using
    Google Cloud Vision AI Safe Search Detection.
    """
    client = get_vision_client()
    image = create_vision_image_object(image_data)

    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    safe_search = response.safe_search_annotation
    return SafeSearchResult(
        adult=safe_search.adult.name,
        spoof=safe_search.spoof.name,
        medical=safe_search.medical.name,
        violence=safe_search.violence.name,
        racy=safe_search.racy.name,
    )
