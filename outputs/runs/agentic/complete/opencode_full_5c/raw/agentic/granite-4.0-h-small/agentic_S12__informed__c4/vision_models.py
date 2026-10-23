from typing import Dict, List


class VisionRequest:
    """Helper for building provider‑specific request payloads.

    Provider implementations can subclass or extend to add provider‑specific fields.
    """

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError


class VisionResponseNormalization:
    """Normalizes raw provider responses to a common internal format.

    Implementations should map provider‑specific fields (e.g., Clarifai 'name',
    Google 'description') to the generic schema used by later‑step scripts.
    """

    @staticmethod
    def normalize_labels(raw: List[Dict]) -> List[str]:
        """Convert a list of label dicts to a list of label strings."""
        return [item["name"] for item in raw]

    @staticmethod
    def normalize_description(raw: str) -> str:
        """Ensure description is a clean string."""
        return str(raw).strip()

    @staticmethod
    def normalize_text(raw: List[Dict]) -> List[str]:
        return [item["description"] for item in raw]

    @staticmethod
    def normalize_safety(raw: bool) -> bool:
        return bool(raw)

    @staticmethod
    def normalize_archives(raw: List[str]) -> List[str]:
        return raw


# Example usage (for later‑step scripts)
# labels = VisionResponseNormalization.normalize_labels(clarifai_response)
# description = VisionResponseNormalization.normalize_description(gemini_response)
# texts = VisionResponseNormalization.normalize_text(vision_text_response)
# safe = VisionResponseNormalization.normalize_safety(anthropic_safety_check)
# archived_paths = VisionResponseNormalization.normalize_archives(object_storage_paths)
