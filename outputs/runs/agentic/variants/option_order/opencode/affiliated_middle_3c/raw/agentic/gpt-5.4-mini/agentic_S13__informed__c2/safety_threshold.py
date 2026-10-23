import requests

from safety_client import PERSPECTIVE_API_URL, get_api_key
from safety_models import build_result


def safety_threshold(text, category_thresholds):
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {name.upper(): {} for name in category_thresholds},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={get_api_key()}", json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    scores = {
        name.lower(): value.get("summaryScore", {}).get("value", 0.0)
        for name, value in data.items()
    }
    labels = [
        name
        for name, threshold in category_thresholds.items()
        if scores.get(name.lower(), 0.0) >= threshold
    ]
    return build_result(not labels, scores, labels)
