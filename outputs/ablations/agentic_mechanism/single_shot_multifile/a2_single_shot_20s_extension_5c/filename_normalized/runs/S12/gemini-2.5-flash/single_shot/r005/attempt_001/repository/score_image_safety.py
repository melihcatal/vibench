import os
from google.cloud import vision_v1p4
from google.cloud.vision_v1p4 import types
from typing import Dict
from vision_client import get_google_vision_client
from vision_models import ImageInput, SafeSearchResult

def score_image_safety(image_input: ImageInput) -> Dict[str, SafeSearchResult]:
    client = get_google_vision_client()

    if image_input.image_bytes:
        image = types.Image(content=image_input.image_bytes)
    elif image_input.image_url:
        image = types.Image(source=types.ImageSource(image_uri=image_input.image_url))
    else:
        raise ValueError("ImageInput must contain either image_bytes or image_url.")

    features = [types.Feature(type_=types.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = types.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    safety_scores = {}
    if response.safe_search_annotation:
        annotation = response.safe_search_annotation
        safety_scores["adult"] = SafeSearchResult(category="adult", likelihood=str(annotation.adult))
        safety_scores["spoof"] = SafeSearchResult(category="spoof", likelihood=str(annotation.spoof))
        safety_scores["medical"] = SafeSearchResult(category="medical", likelihood=str(annotation.medical))
        safety_scores["violence"] = SafeSearchResult(category="violence", likelihood=str(annotation.violence))
        safety_scores["racy"] = SafeSearchResult(category="racy", likelihood=str(annotation.racy))
    return safety_scores