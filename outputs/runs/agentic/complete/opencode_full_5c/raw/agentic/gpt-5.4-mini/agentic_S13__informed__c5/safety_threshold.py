from safety_client import get_client
from safety_models import normalize_thresholds, normalize_text


def safety_threshold(text, thresholds=None):
    client = get_client()
    limits = normalize_thresholds(thresholds)
    raw = client.post(
        "/contentsafety/text:analyze?api-version=2024-09-01",
        {"text": normalize_text(text)},
    )
    cats = raw.get("categoriesAnalysis", [])
    decision = True
    for cat in cats:
        name = str(cat.get("category", "")).lower()
        severity = float(cat.get("severity", 0.0))
        if severity >= limits.get(name, 4.0):
            decision = False
    return {"allow": decision, "raw": raw}
