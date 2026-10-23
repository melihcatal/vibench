# safety_client.py
# [HELPER] Provide local configuration and client helper utilities for Text Content Safety

import os
from typing import Dict, Any

# Provider selection – choose one concrete external provider
# Example: using Azure AI Content Safety (REST)
PROVIDER = "azure"

# Retrieve API key from environment – ensures secrets stay out of code
if PROVIDER == "azure":
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise RuntimeError(
            "Azure Content Safety credentials not set. Define AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )


# Simple helper to create a requests‑style payload for the chosen provider
def build_request_payload(text: str, categories: list = None) -> Dict[str, Any]:
    """Build payload expected by the selected provider.

    Args:
        text: The text to moderate.
        categories: Optional list of categories to check.

    Returns:
        Dictionary ready to be sent as JSON.
    """
    if PROVIDER == "azure":
        payload = {"content": text}
        if categories:
            payload["categories"] = categories
        return payload
    # Add more providers here as needed
    raise ValueError(f"Unsupported provider: {PROVIDER}")


# Simple helper to parse a provider‑specific response into a unified format
# Unified format: {"text": str, "unsafe": bool, "categories": Dict[str, Any]}
def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize moderation response to a common structure.

    Returns:
        A dict with keys "unsafe" (bool) and "categories" (dict of detected issues).
    """
    if PROVIDER == "azure":
        # Azure returns a list of detected issues per category
        unsafe = len(response.get("issues", [])) > 0
        categories = {i["category"]: i for i in response.get("issues", [])}
        return {"unsafe": unsafe, "categories": categories}
    raise ValueError(f"Unsupported provider: {PROVIDER}")
