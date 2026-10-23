import json
from typing import Dict


def translate_payload(
    payload: Dict[str, any], target_lang: str = "es"
) -> Dict[str, any]:
    """Stub for translating message payload text using a managed translation service."""
    # Placeholder: here you would call Google Cloud Translation, AWS Translate,
    # or another provider's SDK.
    # For illustration, we simply append "_translated" to any string fields.
    translated = {}
    for k, v in payload.items():
        if isinstance(v, str):
            translated[k] = f"{v}_translated({target_lang})"
        elif isinstance(v, dict):
            translated[k] = translate_payload(v, target_lang)
        else:
            translated[k] = v
    return translated


def translate_messages(
    messages: List[Dict[str, any]], target_lang: str = "es"
) -> List[Dict[str, any]]:
    """Translate the payload of each message in the batch."""
    return [translate_payload(msg) for msg in messages]
