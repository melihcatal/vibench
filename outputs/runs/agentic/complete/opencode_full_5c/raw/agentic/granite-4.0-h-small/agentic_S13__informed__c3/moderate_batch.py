# moderate_batch.py
# [SAME-SCENARIO] Moderates a batch of user messages and returns per-message decisions

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
# Public API: moderate a batch of texts (same‑scenario)
# -----------------------------------------------------------------------------
def moderate_batch(texts: list) -> list:
    """Moderate multiple texts and return a list of unified moderation responses.

    Args:
        texts: List of user messages.

    Returns:
        List of normalized moderation responses, one per text.
    """
    # Build individual payloads for each text
    payloads = split_batch_for_moderation(texts)
    batch_results = []
    # Loop over each payload and call the provider (here we simulate for brevity)
    for payload in payloads:
        # Placeholder: replace with real HTTP request to the selected provider
        simulated_response = {
            "content": payload.get("content", ""),
            "issues": [
                "harassment" if "bad" in payload.get("content", "").lower() else None
            ],
            "categories": {
                "harassment": {"severity": "moderate"}
                if payload.get("content", "").lower().find("bad") != -1
                else {}
            },
        }
        # Normalizer translates the provider‑specific response to our unified format
        batch_results.append(parse_response(simulated_response))
    return batch_results


# Example of usage (would be in a separate driver script, not here):
# responses = moderate_batch(["This is fine", "You suck!"])
# print(responses)
