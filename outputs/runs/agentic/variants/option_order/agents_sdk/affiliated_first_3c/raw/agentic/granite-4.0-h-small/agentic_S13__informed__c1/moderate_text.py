# [SAME-SCENARIO] moderate_text.py

from safety_client import get_content_safety_client
from safety_models import SafetyRequest, SafetyResponse

# Use AWS Bedrock Guardrails for content safety (scorable provider)
client = get_content_safety_client(
    service="aws",
    endpoint="https://bedrock-runtime.us-east-1.amazonaws.com",
    api_key="${AWS_ACCESS_KEY_ID}",
    secret_key="${AWS_SECRET_ACCESS_KEY}"
)

def moderate_text(user_text: str, unsafe_categories: list = None) -> SafetyResponse:
    """Scores a single user message for policy‑violating content.

    Returns a SafetyResponse containing the overall verdict and per‑category scores.
    """
    request = SafetyRequest(
        text=user_text,
        categories=unsafe_categories or ["harassment", "hate", "self_harm", "sexual", "violence"]
    )
    response = client.moderate(request)
    return response
