from safety_client import get_comprehend_client
from safety_models import BatchModerationRequest, build_decision, normalize_categories


def moderate_batch(payload, config=None):
    request = BatchModerationRequest.from_payload(payload)
    client = get_comprehend_client(config)
    results = []
    for text in request.texts:
        response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
        item = response["ResultList"][0]
        results.append(build_decision(item["Toxicity"] < 0.5, normalize_categories(item.get("Categories", []))))
    return {"results": results}
