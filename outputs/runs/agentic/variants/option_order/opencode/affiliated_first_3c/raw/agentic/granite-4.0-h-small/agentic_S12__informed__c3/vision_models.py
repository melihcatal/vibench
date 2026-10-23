# [HELPER] vision_models.py
# Local models / request/response wrappers for Static Image & Visual Understanding flows
from __future__ import annotations
from typing import Any, Dict, List, Optional


# ----- Normalized Vision Request ----- #
class VisionRequest:
    """Internal representation of a visual analysis request.

    Attributes:
        image_path (str): Local filepath.
        provider (str): Provider identifier used for dispatch.
        options (Dict[str, Any]): Provider‑specific parameters.
    """

    def __init__(self, image_path: str, provider: str, **options: Any):
        self.image_path = image_path
        self.provider = provider
        self.options = options
        # Validate that required env vars exist (delegate to vision_client)
        from .vision_client import load_env_vars

        load_env_vars({provider: os.getenv(provider.upper().replace(" ", "_"))})

    def __repr__(self) -> str:
        return f"VisionRequest({self.provider}, {self.image_path})"


# ----- Normalized Vision Response ----- #
class VisionResponse:
    """Standardized response container for all providers.

    Attributes:
        labels (List[str]): Detected object/label strings.
        description (Optional[str]): Concise visual description.
        text (List[str]): Extracted OCR strings.
        safety (Optional[Dict]): Guardrail safety scores and flags.
    """

    def __init__(
        self,
        labels: List[str] = None,
        description: Optional[str] = None,
        text: List[str] = None,
        safety: Optional[Dict] = None,
    ):
        self.labels = labels if labels is not None else []
        self.description = description
        self.text = text if text is not None else []
        self.safety = safety

    def __repr__(self) -> str:
        return f"VisionResponse(labels={self.labels}, description={self.description}, safety={self.safety})"


# ----- Response Normalizer Functions ----- #
# These simple adapters translate each provider's raw SDK output into the unified VisionResponse shape.
# Implement one per provider as needed.


def normalize_google_vision(response: Any) -> VisionResponse:
    """Map google-cloud-vision label detection response to VisionResponse."""
    labels = [anno.description for anno in response.label_annotations]
    return VisionResponse(labels=labels)


# Placeholder for other normalizers (amazon, azure, IBM) can be added here
