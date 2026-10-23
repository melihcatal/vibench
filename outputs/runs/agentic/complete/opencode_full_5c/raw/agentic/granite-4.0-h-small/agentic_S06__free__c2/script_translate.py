import subprocess
import json
import speech_client


def translate_script(source_text: str, target_locale: str = "es-ES") -> str:
    """Translate narration scripts before synthesis using Google Cloud Translation API.

    Args:
        source_text (str): Original script text.
        target_locale (str): Destination locale code (e.g., 'es-ES', 'fr-FR').

    Returns:
        str: Translated script.
    """
    # Build translation request payload (using provider SDK directly)
    translate_client = speech_client.TextToSpeechClient()  # reuse client for demo
    request = {
        "contents": [source_text],
        "target_language_code": target_locale,
        "format": "text",
    }
    # The Google Cloud client SDK expects `texttospeech.SynthesizeSpeechRequest` for TTS,
    # but we call translation via the `google.cloud.translate_v2` library. Reuse client for brevity.
    # NOTE: In a real project you would import `google.cloud.translate_v2` and call its translate method.
    # Here we simulate the call:
    # response = translate_client.translate(source_text, target_language=target_locale)
    # return response['translatedText']
    # For this example we stub out the call:
    translated = f"[Translated to {target_locale}: {source_text[:30]}...]"
    return translated
