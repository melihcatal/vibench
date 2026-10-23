from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types

from vision_client import create_vision_client, image_path_to_content
from vision_models import (
    ImageRequest,
    SafetyCheckResult,
    SafetyScores,
    evaluate_safety,
    normalize_confidence,
)

_LIKELIHOOD_MAP = {
    vision_types.Likelihood.UNKNOWN: 0.0,
    vision_types.Likelihood.VERY_UNLIKELY: 0.1,
    vision_types.Likelihood.UNLIKELY: 0.3,
    vision_types.Likelihood.POSSIBLE: 0.5,
    vision_types.Likelihood.LIKELY: 0.7,
    vision_types.Likelihood.VERY_LIKELY: 0.95,
}


def _likelihood_to_score(likelihood) -> float:
    return normalize_confidence(_LIKELIHOOD_MAP.get(likelihood, 0.0))


def score_image_safety(request: ImageRequest) -> SafetyCheckResult:
    client: vision_v1.ImageAnnotatorClient = create_vision_client()

    if request.image_bytes:
        image = vision_types.Image(content=request.image_bytes)
    else:
        image = image_path_to_content(request.image_path)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    scores = SafetyScores(
        adult=_likelihood_to_score(safe.adult),
        violence=_likelihood_to_score(safe.violence),
        racy=_likelihood_to_score(safe.racy),
        medical=_likelihood_to_score(safe.medical),
        spoof=_likelihood_to_score(safe.spoof),
    )

    is_safe = evaluate_safety(scores)

    return SafetyCheckResult(
        image_path=request.image_path,
        scores=scores,
        is_safe=is_safe,
    )
