# [LATER-STEP] alt_text_translate.py

import os
from translate_client import TranslateClient
from vision_models import Caption


def translate_caption_en_to_es(caption: Caption) -> str:
    """Translates an English caption into Spanish using a concrete translation service.

    Returns the translated caption text.
    """
    client = TranslateClient()
    # Detects the source language automatically; we explicitly request Spanish (`es`).
    translated = client.translate_text(caption.text, target_language="es")
    return translated


def translate_all_captions(captions: List[Caption]) -> List[str]:
    """Batch‑translate a list of captions."""
    client = TranslateClient()
    return [client.translate_text(c.text, target_language="es") for c in captions]
