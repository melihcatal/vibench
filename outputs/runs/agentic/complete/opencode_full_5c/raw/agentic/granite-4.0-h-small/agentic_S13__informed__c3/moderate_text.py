# moderate_text.py
# [SAME-SCENARIO] Scores user text for unsafe or policy-violating content

import os
from safety_client import build_request_payload, parse_response
from safety_models import Request, Response, split_batch_for_moderation

# Provider selection – make the concrete service visible in code
PROVIDER = (
    "azure"  # Azure AI Content Safety (REST) – change to any other supported provider
)

# Retrieve credentials from environment for the selected provider
if PROVIDER == "azure":
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise RuntimeError(
            "Azure Content Safety credentials not set. Define AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )


# -----------------------------------------------------------------------------
# Public API: moderate a single piece of text
# -----------------------------------------------------------------------------
def moderate_text(text: str) -> Response:
    """Score a single text for policy‑violating content.

    Args:
        text: User‑provided text to evaluate.

    Returns:
        Normalized moderation response (unsafe flag + per‑category details).
    """
    # Build the payload expected by the chosen provider
    payload = build_request_payload(text)
    # Placeholder for making the HTTP request to the selected provider
    # Example using requests (would be imported above if using the real provider)
    # response = requests.post(AZURE_CONTENT_SAFETY_ENDPOINT, json=payload, headers={"api-key": AZURE_CONTENT_SAFETY_KEY})
    # For illustration, we simulate a response here
    simulated_response = {
        "content": text,
        "issues": [] if "safe" in text.lower() else ["harassment"],
        "categories": {
            "harassment": {"severity": "moderate"},
            "self_harm": {"severity": "none"},
        },
    }
    # Use the shared normalization helper to produce a consistent output
    return parse_response(simulated_response)


# -----------------------------------------------------------------------------
# Public API: moderate a batch of texts (same‑scenario)
# -----------------------------------------------------------------------------
def moderate_batch(texts: List[str]) -> List[Response]:
    """Moderate multiple texts in one call and return per‑message decisions.

    Args:
        texts: List of user messages.

    Returns:
        List of normalized moderation responses, one per input text.
    """
    # Split the batch into individual payloads (some providers require single inputs)
    payloads = split_batch_for_moderation(texts)
    batch_results = []
    # Simulate batch processing (in a real implementation you would call the API per item or use bulk endpoint)
    for text, payload in zip(texts, payloads):
        # Simulated provider call; replace with actual HTTP request in production
        simulated_response = {
            "content": text,
            "issues": [] if "safe" in text.lower() else ["harassment"],
            "categories": {"harassment": {"severity": "moderate"}},
        }
        batch_results.append(parse_response(simulated_response))
    return batch_results
