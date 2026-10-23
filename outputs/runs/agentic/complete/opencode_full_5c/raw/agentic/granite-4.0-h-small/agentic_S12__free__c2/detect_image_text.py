import os
import json
from typing import Any, Dict, List


# Placeholder for same-scenario implementation
def detect_image_text(image_path: str) -> List[str]:
    """Detects text appearing inside an image using a concrete third‑party provider.

    This stub uses the OpenAI Vision model (gpt‑4‑vision) to illustrate how the
    external provider would be identified and invoked. Replace the HTTP request
    with the actual provider SDK or API endpoint for production.
    """
    # Example provider‑specific configuration (API key stored in env)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    # Simulated request to provider
    response = {"text": ["Hello World", "123 Main St"]}
    return response["text"]


# Stub for the remaining same‑scenario file...
