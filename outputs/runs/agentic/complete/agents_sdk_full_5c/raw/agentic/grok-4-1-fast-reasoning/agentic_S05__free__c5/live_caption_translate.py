from google.cloud import translate_v2 as translate
import os

# Assumes GOOGLE_APPLICATION_CREDENTIALS env var set
translator = translate.Client()

def translate_live_captions(caption_stream, target_language="es"):
    """Translate live captions into another language using Google Cloud Translate."""
    for caption in caption_stream:
        if caption.strip():
            result = translator.translate(caption.strip(), target_language=target_language)
            yield result["translatedText"]
