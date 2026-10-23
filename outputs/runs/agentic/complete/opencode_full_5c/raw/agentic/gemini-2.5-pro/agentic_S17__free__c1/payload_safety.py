from security_client import get_perspective_client
from security_models import SafetyCheckRequest, SafetyCheckResponse


def check_payload_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    perspective_client = get_perspective_client()

    analyze_request = {
        "comment": {"text": request.content},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    response = perspective_client.comments().analyze(body=analyze_request).execute()

    scores = {}
    is_safe = True

    for attr, values in response["attributeScores"].items():
        score_value = values["summaryScore"]["value"]
        scores[attr] = score_value
        if score_value > request.threshold:
            is_safe = False

    return SafetyCheckResponse(is_safe=is_safe, scores=scores)
