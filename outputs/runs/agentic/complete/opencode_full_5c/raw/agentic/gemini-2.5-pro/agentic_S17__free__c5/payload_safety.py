from security_client import get_perspective_client
from security_models import ContentSafetyRequest, ContentSafetyResponse


def check_payload_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    """Checks decrypted text payloads for unsafe content using the Perspective API."""
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response["attributeScores"].items():
        scores[attribute] = data["summaryScore"]["value"]

    return ContentSafetyResponse(scores=scores)
