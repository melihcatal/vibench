from typing import Any, Dict

# ----------------------------------------------------------------------
# vision_models.py – Request, response, and normalization helpers
# ----------------------------------------------------------------------


def normalize_vision_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Translate a generic request to the provider‑specific shape.

    Example: convert a unified `image_path` key to the provider's `image_url`.
    """
    # Stub – replace with concrete mapping when you select a provider
    return payload


def parse_vision_response(raw: Dict[str, Any]) -> Any:
    """Extract useful fields from the provider's raw response.

    Returns a simplified dict, e.g., {'labels': [...], 'confidence': ...}
    """
    # Stub – adjust to match the real provider schema
    return raw


def load_local_config() -> Dict[str, Any]:
    """Load provider credentials from environment variables or a .env file.

    Returns a dict with keys required by `construct_client` in vision_client.py.
    """
    return {
        "endpoint": os.getenv("ALIBABA_VISION_ENDPOINT"),
        "access_key_id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    }
