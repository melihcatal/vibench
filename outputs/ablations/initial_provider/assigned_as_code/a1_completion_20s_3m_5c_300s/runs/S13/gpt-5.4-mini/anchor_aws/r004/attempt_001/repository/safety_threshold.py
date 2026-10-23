from safety_client import create_comprehend_client
from safety_models import normalize_categories


def safety_threshold(payload, config=None):
    client = create_comprehend_client(config)
    data = payload or {}
    text = data.get("text", "")
    thresholds = normalize_categories(data.get("thresholds"))
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
    scores = {}
    for item in response.get("ResultList", []):
        for label in item.get("Labels", []):
            scores[label.get("Name", "unknown").lower()] = float(label.get("Score", 0))
    allow = all(scores.get(category, 0.0) < threshold for category, threshold in thresholds.items())
    return {"allow": allow, "scores": scores}
