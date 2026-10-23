from typing import Dict, Any
import deep_translator

"""Translate customer-facing message payload text using DeepL API."""

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")

translator = deep_translator.DeepL(auth_key=DEEPL_AUTH_KEY, target_lang="EN")


def translate_payload_text(
    payload: Dict[str, Any], target_lang: str = "EN"
) -> Dict[str, Any]:
    """Translate the 'text' field in payload and return new payload."""
    original = payload.get("text", "")
    if not original:
        return payload  # nothing to translate
    translated = translator.translate(original, target_lang=target_lang)
    new_payload = payload.copy()
    new_payload["text"] = translated
    return new_payload


# Example batch translation helper


def translate_batch(
    messages: List[Dict[str, Any]], target_lang: str = "EN"
) -> List[Dict[str, Any]]:
    return [translate_payload_text(msg, target_lang) for msg in messages]


# No return needed for the tool, just write the file
