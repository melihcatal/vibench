from safety_client import get_comprehend_client
from safety_models import TextModerationRequest, build_decision, normalize_categories


def safety_threshold(payload, config=None):
    request = TextModerationRequest.from_payload(payload)
    thresholds = (payload or {}).get("thresholds") or {}
    client = get_comprehend_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": request.text}], LanguageCode="en")
    item = response["ResultList"][0]
    categories = normalize_categories(item.get("Categories", []))
    allow = True
    for name, score in categories.items():
        if score >= float(thresholds.get(name, 0.5)):
            allow = False
    return build_decision(allow, categories)
