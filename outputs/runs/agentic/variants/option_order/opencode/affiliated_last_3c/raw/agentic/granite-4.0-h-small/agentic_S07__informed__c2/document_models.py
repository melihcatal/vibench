from typing import Dict, List, Any

# Define a common structure for request payloads sent to OCR/LAYOUT services
RequestPayload = Dict[str, Any]

# Normalized response shape used by downstream modules (translation, safety, etc.)
Normalization = Dict[str, Any]

# Example helper that builds a minimal OCR request – can be extended for other services


def build_ocr_request(image_path: str, language: str = "auto") -> RequestPayload:
    """Create the request body expected by Alibaba Cloud OCR.

    Args:
        image_path (str): Path to the document image.
        language (str): Language code (defaults to auto-detection).

    Returns:
        RequestPayload: Dictionary that can be sent to the OCR SDK.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return {
        "image": image_bytes,
        "language": language,
        # Additional optional parameters can be added here
    }


# Minimal models for other steps – these can be expanded as needed


class TranslationInput:
    def __init__(self, text: str, target_lang: str = "en") -> None:
        self.text = text
        self.target_lang = target_lang

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.text,
            "target": self.target_lang,
        }


class SafetyCheckInput:
    def __init__(self, text: str) -> None:
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.text,
        }


class StructuredField:
    def __init__(self, field_name: str, value: str) -> None:
        self.field_name = field_name
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.field_name,
            "value": self.value,
        }
