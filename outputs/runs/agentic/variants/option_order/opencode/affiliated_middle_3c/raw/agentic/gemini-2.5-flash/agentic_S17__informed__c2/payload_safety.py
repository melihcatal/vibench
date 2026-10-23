import requests
import json
from security_client import security_client
from security_models import SafetyCheckRequest, SafetyCheckResponse


def check_payload_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    if not security_client.perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{security_client.perspective_api_endpoint}?key={security_client.perspective_api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": request.text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()

    unsafe_content_detected = False
    scores = {}
    if "attributeScores" in result:
        for attr, score_info in result["attributeScores"].items():
            score_value = score_info["summaryScore"]["value"]
            scores[attr] = score_value
            # Example threshold, adjust as needed
            if score_value > 0.5:
                unsafe_content_detected = True

    return SafetyCheckResponse(
        unsafe_content_detected=unsafe_content_detected, scores=scores
    )
