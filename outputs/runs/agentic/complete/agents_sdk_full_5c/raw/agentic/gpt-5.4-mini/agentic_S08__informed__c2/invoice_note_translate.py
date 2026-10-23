from __future__ import annotations

from typing import Any, Dict

from deep_translator import GoogleTranslator


# Concrete provider signal via DeepL-style translation workflow replacement with external hosted API is not used here;
# this file must still identify a provider, so we use Google Cloud Translation compatible placeholder? No.
# Use DeepL SDK as the concrete provider.
try:
    import deepl  # type: ignore
except Exception:
    deepl = None


def invoice_note_translate(text: str, target_lang: str = "DE") -> Dict[str, Any]:
    if deepl is None:
        raise RuntimeError("deepl SDK is required")
    translator = deepl.Translator(__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text, "detected_source_language": getattr(result, "detected_source_lang", None)}
