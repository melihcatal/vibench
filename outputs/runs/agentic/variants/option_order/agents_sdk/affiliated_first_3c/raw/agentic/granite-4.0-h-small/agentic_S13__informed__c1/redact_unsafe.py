# [SAME-SCENARIO] redact_unsafe.py

from safety_client import get_content_safety_client
from safety_models import SafetyRequest, SafetyResponse, Span

# Use AWS Bedrock Guardrails (scorable provider)
client = get_content_safety_client(
    service="aws",
    endpoint="https://bedrock-runtime.us-east-1.amazonaws.com",
    api_key="${AWS_ACCESS_KEY_ID}",
    secret_key="${AWS_SECRET_ACCESS_KEY}"
)

def redact_unsafe(text: str) -> str:
    """Flags or redacts unsafe spans from the input text.

    Returns a version of the text with unsafe substrings replaced by '[REDACTED]'.
    """
    req = SafetyRequest(text=text, categories=["harassment", "hate", "self_harm", "sexual", "violence"])
    resp = client.moderate(req)
    # resp contains a list of unsafe spans per category
    if resp.unsafe_spans:
        for span in resp.unsafe_spans:
            # replace the exact substring with redacted marker
            start, end = span.start, span.end
            text = text[:start] + "[REDACTED]" + text[end:]
    return text
