# [HELPER] translation_models.py

from typing import Dict, Any

# Constants for model identification (placeholder, as Google Cloud Translation does not expose model names)
DEFAULT_MODEL = "default"


def get_model_identifier(model: str = DEFAULT_MODEL) -> str:
    """Return a standardized identifier for a translation model.

    Args:
        model (str): Optional custom model name; defaults to provider’s default.

    Returns:
        str: Model identifier recognized by the helper layer.
    """
    return model


# Mapping of payload structures to provider expectations (example for Google Cloud Translation)
def build_input(text: str, target_language: str = "es") -> Dict[str, Any]:
    """Build payload compatible with the configured provider.

    Args:
        text (str): Source text.
        target_language (str): Target language code.

    Returns:
        Dict[str, Any]: Normalized input dictionary.
    """
    return {"q": text, "target": target_language}


# Normalize the provider’s response into a consistent shape


def parse_output(raw: Dict[str, Any]) -> Dict[str, str]:
    """Normalize a raw provider response.

    Args:
        raw (Dict[str, Any]): Unprocessed response object.

    Returns:
        Dict[str, str]: Unified response with a single key 'translatedText'.
    """
    return {"translatedText": raw.get("translatedText", "")}


# Local testing hook
if __name__ == "__main__":
    example = build_input("Welcome!", target_language="fr")
    print("Built request:", example)
