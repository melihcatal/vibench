from safety_client import get_comprehend_client
from safety_models import TextModerationRequest, normalize_categories


def redact_unsafe(payload, config=None):
    request = TextModerationRequest.from_payload(payload)
    client = get_comprehend_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": request.text}], LanguageCode="en")
    item = response["ResultList"][0]
    spans = []
    for category in item.get("Categories", []):
        if float(category.get("Score", 0.0)) >= 0.5:
            spans.append(category.get("Name"))
    return {"redacted_text": request.text, "unsafe_categories": spans, "categories": normalize_categories(item.get("Categories", []))}
