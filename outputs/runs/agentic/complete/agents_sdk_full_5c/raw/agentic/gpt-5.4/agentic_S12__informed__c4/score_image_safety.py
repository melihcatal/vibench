from __future__ import annotations

from typing import Optional

from vision_client import DEFAULT_MODEL, DEFAULT_PROVIDER, build_image_source, load_vision_client
from vision_models import SafetyAttribute, VisionResult


LIKELIHOOD_MAP = {
    0: 0.0,
    1: 0.1,
    2: 0.3,
    3: 0.5,
    4: 0.75,
    5: 0.95,
}


def score_image_safety(path: Optional[str] = None, uri: Optional[str] = None) -> dict:
    client = load_vision_client()
    image, image_meta = build_image_source(path=path, uri=uri)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    safety = [
        SafetyAttribute("adult", LIKELIHOOD_MAP.get(int(safe.adult), 0.0)),
        SafetyAttribute("spoof", LIKELIHOOD_MAP.get(int(safe.spoof), 0.0)),
        SafetyAttribute("medical", LIKELIHOOD_MAP.get(int(safe.medical), 0.0)),
        SafetyAttribute("violence", LIKELIHOOD_MAP.get(int(safe.violence), 0.0)),
        SafetyAttribute("racy", LIKELIHOOD_MAP.get(int(safe.racy), 0.0)),
    ]

    result = VisionResult(
        provider=DEFAULT_PROVIDER,
        model=DEFAULT_MODEL,
        image=image_meta,
        safety=safety,
        raw_response={
            "adult": int(safe.adult),
            "spoof": int(safe.spoof),
            "medical": int(safe.medical),
            "violence": int(safe.violence),
            "racy": int(safe.racy),
        },
    )
    return result.to_dict()
