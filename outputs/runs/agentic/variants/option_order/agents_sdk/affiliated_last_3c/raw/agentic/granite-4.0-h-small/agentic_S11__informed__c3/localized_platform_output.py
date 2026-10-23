import json
from model_models import ModelInvocationResponse
from typing import Dict

def localized_platform_output(raw_response: ModelInvocationResponse, target_locale: str = "es") -> Dict[str, Any]:
    """
    Translate the generated text into another locale using DeepL API.
    Returns a dict containing the original text, the translated text, and
    translation metadata.
    """
    import deepl
    # DeepL free tier requires an auth key; env variable DEEPL_AUTH_KEY must be set.
    translator = deepl.Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    try:
        translation = translator.translate_text(
            raw_response.text,
            target_lang=target_locale
        )
    except Exception as exc:
        # Fallback if translation fails
        return {
            "text": raw_response.text,
            "translated": None,
            "translation_error": str(exc)
        }
    return {
        "text": raw_response.text,
        "translated": translation.text,
        "source_lang": "en",  # assumed source language
        "target_lang": target_locale,
        "translation_details": {
            "source_word_count": len(raw_response.text.split()),
            "target_word_count": len(translation.text.split())
        }
    }

# Example script entry point
if __name__ == "__main__":
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("DEPLOYMENT_ID must be set.")
    prompt = "The quick brown fox jumps over the lazy dog."
    response = collect_platform_metadata(deployment, prompt)
    localized = localized_platform_output(response, target_locale="es")
    print(json.dumps(localized, indent=2))
