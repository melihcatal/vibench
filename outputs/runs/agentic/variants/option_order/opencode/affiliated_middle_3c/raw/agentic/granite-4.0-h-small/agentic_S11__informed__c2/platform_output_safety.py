import os
import re
from typing import Any
from model_client import ManagedModelClient
from model_models import InferenceResponse
from select_platform_resource import select_provider


def detect_unsafe_content(text: str) -> bool:
    """Simple heuristic to detect potentially unsafe content (e.g., hate, harassment, sexual content)."""
    unsafe_patterns = [
        re.compile(r"\b(hate|kill|fuck|nigga|bitch|slut|pussy)\b", re.IGNORECASE),
        re.compile(r"\b(\d{3}-\d{2}-\d{4})\b"),  # detect SSN-like patterns
    ]
    for pattern in unsafe_patterns:
        if pattern.search(text):
            return True
    return False


def platform_output_safety_check(provider: str, response: InferenceResponse) -> bool:
    """Check model output for unsafe content using a generic heuristic. Returns True if safe."""
    if detect_unsafe_content(response["text"]):
        print("[WARNING] Unsafe content detected in platform response")
        return False
    return True


def main():
    # Example configuration (populate with real provider-specific settings)
    config = {
        "provider": "huggingface",
        "model_id": "your-model-id",
        "hf_token": os.getenv("HF_TOKEN"),
    }
    client = ManagedModelClient(config)
    response = client.invoke({"prompt": "Hello, how are you?"})
    if platform_output_safety_check(config["provider"], response):
        print("Output is safe.")
    else:
        print("Output rejected due to unsafe content.")


if __name__ == "__main__":
    main()
