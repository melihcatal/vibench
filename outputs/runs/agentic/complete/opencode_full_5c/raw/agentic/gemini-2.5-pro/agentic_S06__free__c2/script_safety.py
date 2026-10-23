from speech_client import get_perspective_client
from speech_models import SafetyCheckRequest


def check_script_safety(request: SafetyCheckRequest) -> dict:
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    return response
