# [SAME-SCENARIO] moderate_batch.py

from safety_client import get_content_safety_client
from safety_models import SafetyRequestBatch, SafetyResponseBatch

# Use AWS Bedrock Guardrails (scorable provider)
client = get_content_safety_client(
    service="aws",
    endpoint="https://bedrock-runtime.us-east-1.amazonaws.com",
    api_key="${AWS_ACCESS_KEY_ID}",
    secret_key="${AWS_SECRET_ACCESS_KEY}"
)

def moderate_batch(texts: list[str], unsafe_categories: list = None) -> SafetyResponseBatch:
    """Moderates a list of messages and returns per‑message decisions.

    Returns a SafetyResponseBatch with a result for each input text.
    """
    batch = SafetyRequestBatch(
        inputs=[SafetyRequest(text=t, categories=unsafe_categories) for t in texts]
    )
    response = client.moderate_batch(batch)
    return response
