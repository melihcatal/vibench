import os
from speech_models import ensure_speak_wrapper
from speech_client import get_tts_client
from google.cloud import translate_v2 as translate

def translate_script(source_text: str, target_lang: str = "es") -> str:
    """Translate plain narration script to the target language.

    Args:
        source_text: Narration script in source language.
        target_lang: ISO‑9171 language code (e.g., 'es', 'fr').

    Returns:
        Translated script ready for TTS.
    """
    # Use Google Cloud Translation API (concrete provider signal)
    translate_client = translate.Client()
    result = translate_client.translate(source_text, target_language=target_lang)
    translated = result["translatedText"]
    # Ensure the output is wrapped with <speak> for SSML synthesis
    return ensure_speak_wrapper(translated)

if __name__ == "__main__":
    demo = "Welcome to the demonstration. Let's convert this English script to Spanish."
    spanish_script = translate_script(demo, target_lang="es")
    print("Translated SSML:", spanish_script)
