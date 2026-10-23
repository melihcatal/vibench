# [LATER-STEP] alt_text_translate.py

import os
from google.cloud import translate_v2 as translate
from vision_models import DetectedText
from google.auth import exceptions as gauth_exc


def translate_alt_text(
    detected_texts: List[DetectedText], target_lang: str = "es"
) -> List[DetectedText]:
    """Translate generated image descriptions (alt text) to a target language using Google Cloud Translation.","""
    # Initialize client - credentials come from GOOGLE_APPLICATION_CREDENTIALS env var
    try:
        client = translate.Client()
    except gauth_exc.GoogleAuthError:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point to JSON credential file."
        )
    translated = []
    for txt in detected_texts:
        result = client.translate(txt.text, target_language=target_lang)
        translated.append(
            DetectedText(text=result["translatedText"], bounding_box=txt.bounding_box)
        )
    return translated
