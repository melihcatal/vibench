from typing import Any, Dict

from vision_client import as_image_payload, rekognition_client, load_vision_config
from vision_models import normalize_labels


def detect_image_labels(image: Any) -> Dict[str, Any]:
    cfg = load_vision_config()
    client = rekognition_client(cfg.region_name)
    response = client.detect_labels(
        Image=as_image_payload(image),
        MaxLabels=cfg.max_labels,
        MinConfidence=cfg.min_confidence,
    )
    return normalize_labels(response).__dict__
