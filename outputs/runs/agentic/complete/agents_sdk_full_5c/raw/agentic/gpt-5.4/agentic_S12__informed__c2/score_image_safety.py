from __future__ import annotations

from typing import Dict, Any

from vision_client import VisionClientFactory, build_vision_image, GOOGLE_VISION_MODEL, GOOGLE_VISION_PROVIDER
from vision_models import ImageSource, SafetyCategoryScore, VisionResult, normalize_confidence

_SAFE_SEARCH_FIELDS = {
    "adult": "adult",
    "spoof": "spoof",
    "medical": "medical",
    "violence": "violence",
    "racy": "racy",
}

_LIKELIHOOD_TO_SCORE = {
    0: 0.0,
    1: 0.05,
    2: 0.2,
    3: 0.5,
    4: 0.75,
    5: 0.95,
}


def score_image_safety(source: ImageSource) -> Dict[str, Any]:
    client = VisionClientFactory.create_image_annotator_client()
    image = build_vision_image(source)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    scores = []
    for category_name, field_name in _SAFE_SEARCH_FIELDS.items():
        likelihood_value = int(getattr(safe, field_name))
        scores.append(
            SafetyCategoryScore(
                category=category_name,
                confidence=normalize_confidence(_LIKELIHOOD_TO_SCORE.get(likelihood_value, 0.0)),
            )
        )
    result = VisionResult(
        provider=GOOGLE_VISION_PROVIDER,
        model=GOOGLE_VISION_MODEL,
        safety_scores=scores,
        raw_response={"safe_search": {name: int(getattr(safe, field)) for name, field in _SAFE_SEARCH_FIELDS.items()}},
    )
    return result.to_dict()
