from model_models import InferenceResponse
import json

def translate_output(raw_text: str, target_lang: str = "es") -> str:
    """Translate generated model output to a target language using a hosted translation model.

    Args:
        raw_text: The original model output.
        target_lang: ISO language code (default: 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Placeholder: replace with a real translation service call (e.g., Google Translate, DeepL).
    # Here we simulate a translation by prefixing the target language code.
    return f"[Translated to {target_lang.upper()}] {raw_text}"
