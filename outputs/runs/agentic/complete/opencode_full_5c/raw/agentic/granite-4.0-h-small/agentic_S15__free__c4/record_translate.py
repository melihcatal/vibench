# [LATER-STEP] record_translate.py
"""Utility to translate user‑facing fields in a document.

This stub demonstrates how a translation provider (e.g., Amazon Translate,
Google Translate, or OpenAI's translation model) could be called.
In production, replace the stub with an actual SDK call and proper error handling.
"""

from typing import Any, Dict

GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_document(
    document: Dict[str, Any], target_lang: str = "es"
) -> Dict[str, Any]:
    """Translate the 'content' field of the document to the target language.

    Returns a new document dict with an added 'content_{target_lang}' field
    containing the translated text. The original content is preserved.
    """
    content = document.get("content")
    if not content:
        return document  # nothing to translate
    # ------------------- Provider placeholder -------------------
    # Example using Google Translate REST API (replace with actual SDK if desired)
    payload = {
        "q": content,
        "target": target_lang,
        "format": "text",
        "key": "YOUR_API_KEY",  # <-- replace with real key or env var
    }
    # NOTE: In real code, perform an HTTP request and handle errors.
    # For this example we simply echo back the original text with a suffix.
    translated = f"{content} (translated to {target_lang})"
    # ----------------------------------------------------------------
    new_doc = document.copy()
    new_doc[f"content_{target_lang}"] = translated
    return new_doc
