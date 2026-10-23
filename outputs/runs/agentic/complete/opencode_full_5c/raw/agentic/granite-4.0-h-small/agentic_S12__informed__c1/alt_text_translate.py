import json
from typing import Dict

# ----------------------------------------------------------------------
# alt_text_translate.py – Translate image captions into other languages
# ----------------------------------------------------------------------

# Placeholder for a translation SDK; example uses Google Cloud Translation.
try:
    from google.cloud import translate_v2 as translate

    translator = translate.Client()
except Exception:
    # Fallback to a minimal dummy implementation if SDK unavailable
    translator = None


def translate_caption(caption: str, target_lang: str = "es") -> str:
    """Translate a short image description to the target language.

    Args:
        caption: The original English description.
        target_lang: ISO language code (default Spanish).

    Returns:
        Translated description.
    """
    if translator is None:
        # Simple dummy echo for demo purposes
        return f"[Translated to {target_lang}] {caption}"
    response = translator.translate(caption, target_language=target_lang)
    return response.get("translatedText", caption)


if __name__ == "__main__":
    sample = {"description": "A sunny day with a parked car under a tree."}
    translated = translate_caption(sample["description"], target_lang="fr")
    print(json.dumps({"translated_caption": translated}, ensure_ascii=False, indent=2))
