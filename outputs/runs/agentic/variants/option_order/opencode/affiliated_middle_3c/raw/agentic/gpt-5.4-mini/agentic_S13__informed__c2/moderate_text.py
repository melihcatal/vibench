import requests

from safety_client import PERSPECTIVE_API_URL, base_payload, get_api_key
from safety_models import build_result


def moderate_text(text, threshold=0.5):
    payload = base_payload(text)
    payload["doNotStore"] = True
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={get_api_key()}", json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    scores = {
        name.lower(): value.get("summaryScore", {}).get("value", 0.0)
        for name, value in data.items()
    }
    labels = [name for name, score in scores.items() if score >= threshold]
    return build_result(not labels, scores, labels)
