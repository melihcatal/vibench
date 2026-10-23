import os
from google.cloud import vision
from vision_models import ImageAnalysisRequest, SafetyScoreResult

def score_image_safety(request: ImageAnalysisRequest) -> SafetyScoreResult:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = request.image_url

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Google Cloud Vision API returns likelihood values (UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)
    # We need to map these to a simple score and categories.
    likelihood_map = {
        vision.Likelihood.UNKNOWN: "unknown",
        vision.Likelihood.VERY_UNLIKELY: "very_unlikely",
        vision.Likelihood.UNLIKELY: "unlikely",
        vision.Likelihood.POSSIBLE: "possible",
        vision.Likelihood.LIKELY: "likely",
        vision.Likelihood.VERY_LIKELY: "very_likely",
    }

    categories = []
    overall_score = "safe"

    if safe_search_annotation.adult == vision.Likelihood.POSSIBLE or \
       safe_search_annotation.adult == vision.Likelihood.LIKELY or \
       safe_search_annotation.adult == vision.Likelihood.VERY_LIKELY:
        categories.append(f"adult: {likelihood_map[safe_search_annotation.adult]}")
        overall_score = "unsafe"

    if safe_search_annotation.violence == vision.Likelihood.POSSIBLE or \
       safe_search_annotation.violence == vision.Likelihood.LIKELY or \
       safe_search_annotation.violence == vision.Likelihood.VERY_LIKELY:
        categories.append(f"violence: {likelihood_map[safe_search_annotation.violence]}")
        overall_score = "unsafe"

    if safe_search_annotation.racy == vision.Likelihood.POSSIBLE or \
       safe_search_annotation.racy == vision.Likelihood.LIKELY or \
       safe_search_annotation.racy == vision.Likelihood.VERY_LIKELY:
        categories.append(f"racy: {likelihood_map[safe_search_annotation.racy]}")
        if overall_score != "unsafe": # Don't downgrade from unsafe if already set
            overall_score = "potentially_unsafe"

    if safe_search_annotation.medical == vision.Likelihood.POSSIBLE or \
       safe_search_annotation.medical == vision.Likelihood.LIKELY or \
       safe_search_annotation.medical == vision.Likelihood.VERY_LIKELY:
        categories.append(f"medical: {likelihood_map[safe_search_annotation.medical]}")
        if overall_score == "safe": # If nothing else triggered, medical isn't necessarily unsafe
            overall_score = "safe"

    if safe_search_annotation.spoof == vision.Likelihood.POSSIBLE or \
       safe_search_annotation.spoof == vision.Likelihood.LIKELY or \
       safe_search_annotation.spoof == vision.Likelihood.VERY_LIKELY:
        categories.append(f"spoof: {likelihood_map[safe_search_annotation.spoof]}")
        if overall_score == "safe":
            overall_score = "potentially_unsafe"

    # If no specific unsafe content is detected, and there are no categories, it's safe.
    if not categories and overall_score == "safe":
        overall_score = "safe"

    return SafetyScoreResult(score=overall_score, categories=categories)
