import requests
from model_client import get_perspective_api_key
from model_models import SafetyCheckRequest, SafetyCheckResponse


def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    api_key = get_perspective_api_key()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": request.text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    toxicity_score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )

    is_safe = toxicity_score < 0.7

    scores = {"toxicity": toxicity_score}

    return SafetyCheckResponse(is_safe=is_safe, scores=scores, raw_response=data)
