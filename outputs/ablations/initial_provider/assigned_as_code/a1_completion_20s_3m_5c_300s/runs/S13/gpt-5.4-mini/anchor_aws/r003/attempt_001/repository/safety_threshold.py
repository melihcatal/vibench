from safety_client import get_comprehend_client
from safety_models import normalize_thresholds, normalize_text_payload


def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = normalize_thresholds(payload)
    if config:
        thresholds.update(normalize_thresholds(config))
    normalized = normalize_text_payload(payload)
    client = get_comprehend_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": normalized.get("text", "")}], LanguageCode=config.get("language", "en"))
    score = response.get("ResultList", [{}])[0].get("Toxicity", 0)
    limit = thresholds.get("toxicity", config.get("threshold", 0.5))
    return {"allowed": score < limit, "toxicity": score, "threshold": limit}
