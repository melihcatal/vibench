import requests
import os
from security_client import get_perspective_api_client
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    api_key, api_endpoint = get_perspective_api_client()

    analyze_request = {
        "comment": {"text": request.payload_text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    response = requests.post(f"{api_endpoint}?key={api_key}", json=analyze_request)
    response.raise_for_status()
    result = response.json()

    toxicity_score = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    is_safe = toxicity_score < 0.5  # Example threshold

    return PayloadSafetyResponse(unsafe_score=toxicity_score, is_safe=is_safe)
