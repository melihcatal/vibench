from safety_client import get_comprehend_client
from safety_models import normalize_thresholds, normalize_text


def safety_threshold(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    thresholds = normalize_thresholds(config.get("thresholds", {}))
    text = normalize_text(payload.get("text"))
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode=config.get("language", "en"))
    result = response.get("ResultList", [{}])[0]
    score = result.get("Toxicity", 0)
    threshold = thresholds.get("toxicity", config.get("threshold", 0.5))
    return {"allow": score < threshold, "score": score, "threshold": threshold}
