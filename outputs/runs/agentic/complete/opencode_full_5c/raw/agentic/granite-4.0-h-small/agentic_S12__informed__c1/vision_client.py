import os
from typing import Any, Dict

# ----------------------------------------------------------------------
# vision_client.py – Local configuration and client helper utilities
# ----------------------------------------------------------------------


def load_config() -> Dict[str, Any]:
    """Load service credentials from environment variables.

    Uses Alibaba Cloud Vision as the concrete provider. The identifiers
    are the environment variables required by the Alibaba SDK.
    """
    return {
        "endpoint": os.getenv("ALIBABA_VISION_ENDPOINT"),
        "access_key_id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    }


def construct_client(config: Dict[str, Any]) -> Any:
    """Construct and return a client object using Alibaba Cloud SDK.

    Returns an instance of `VisionService` (placeholder name) that can be
    called directly for label detection, OCR, moderation, etc.
    """
    # Placeholder import – replace with the actual SDK import in production
    from alibabacloud_vision import VisionService

    svc = VisionService(**config)
    return svc
