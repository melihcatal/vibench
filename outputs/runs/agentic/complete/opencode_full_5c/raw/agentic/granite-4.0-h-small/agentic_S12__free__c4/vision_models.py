# vision_models.py
# LOCAL HELPER - Static Image and Visual Understanding

from typing import List, Dict, Any

# Request & response wrappers (provider-agnostic) for image analysis


class ImageAnnotateRequest:
    """Wrapper to build request payload for image analysis."""

    def __init__(self, image_bytes: bytes, features: List[Dict[str, Any]]):
        self.image_bytes = image_bytes
        self.features = features


class ImageAnnotateResponse:
    """Wrapper for parsed response from a vision provider."""

    def __init__(self, raw_response: Any):
        self.raw = raw_response
        self.labels = []
        self.description = ""
        self.text = ""
        self.safe = True
        self._parse()

    def _parse(self):
        # Example parsing logic for Google Cloud Vision
        # Replace with provider-specific extraction if needed
        self.labels = [
            annotation.description for annotation in self.raw.label_annotations
        ]
        self.description = self.raw.description  # placeholder
        self.text = ""  # placeholder for OCR text
        # Simple safety check based on detected violent or adult content
        self.safe = not any(
            annotation.score > 0.7  # arbitrary threshold
            for annotation in self.raw.safe_search_annotation
        )


# Normalization helpers (convert provider-specific objects to internal model)
def normalize_response(provider_name: str, raw: Any) -> ImageAnnotateResponse:
    if provider_name == "Google Cloud Vision":
        return ImageAnnotateResponse(raw)
    raise ValueError(f"Unsupported provider: {provider_name}")
