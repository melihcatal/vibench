import requests
from translation_client import get_perspective_api_key

TOXICITY_ATTRIBUTE = "TOXICITY"


def check_unsafe_content(text: str) -> dict:
    api_key = get_perspective_api_key()
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY not set"}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"comment": {"text": text}, "requestedAttributes": {TOXICITY_ATTRIBUTE: {}}}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    toxicity_score = (
        result.get("attributeScores", {})
        .get(TOXICITY_ATTRIBUTE, {})
        .get("summaryScore", {})
        .get("value")
    )

    return {
        "toxicity_score": toxicity_score,
        "attributes": result.get("attributeScores"),
    }
