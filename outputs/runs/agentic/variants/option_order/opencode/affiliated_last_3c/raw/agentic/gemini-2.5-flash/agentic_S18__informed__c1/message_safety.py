import requests
from messaging_client import get_perspective_api_key
from messaging_models import MessageSafetyRequest

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_message_safety(request: MessageSafetyRequest) -> dict:
    api_key = get_perspective_api_key()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": api_key}
    payload = {
        "comment": {"text": request.text_content},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(PERSPECTIVE_API_BASE_URL, params=params, json=payload)
    response.raise_for_status()

    result = response.json()
    toxicity_score = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
    )

    return {"toxicity_score": toxicity_score, "raw_response": result}
