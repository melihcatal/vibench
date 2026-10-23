import os
from typing import Dict, Any

# Helper utilities for all vision‑related integration files


def load_config() -> Dict[str, Any]:
    """Load runtime configuration (API keys, endpoint URLs, etc.) from environment variables or a config file."""
    return {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    }


def build_vision_request(image_path: str, model: str, **kwargs) -> Dict[str, Any]:
    """Normalize a request payload for the concrete provider."""
    cfg = load_config()
    return {
        "model": model,
        "prompt": f"Analyze the image at {image_path}.",
        "image": {"path": image_path},
        **kwargs,
    }


def parse_vision_response(raw: Dict[str, Any]) -> Any:
    """Parse and standardize the provider's JSON response into our internal schema."""
    # Example: extract relevant fields from raw response
    return {
        "labels": raw.get("labels", []),
        "description": raw.get("description", ""),
        "text": raw.get("text", []),
        "safe": raw.get("safe", False),
    }


# Export helpers for later‑step files
__all__ = ["load_config", "build_vision_request", "parse_vision_response"]
