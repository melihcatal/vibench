import os
import json
import sys
from google.cloud import translate_v2 as translate  # provider: Google Cloud Translation

from speech_client import get_client
from speech_models import SynthesisRequest, SynthesisResponse, normalize_request

def translate_narration(script_text: str, target_lang: str = "es") -> str:
    """Translate a narration script using Google Cloud Translation API.

    Args:
        script_text (str): Original script in source language.
        target_lang (str, optional): ISO language code for target, default 'es'.

    Returns:
        str: Translated script ready for synthesis.
    """
    translate_client = translate.Client()
    result = translate_client.translate(script_text, target_language=target_lang)
    return result["translatedText"]


def synthesize_translated(script_text: str, target_lang: str = "es", voice_name: str = None):
    """Translate then synthesize the script in a single workflow.

    Exposes helper functions from other modules for a realistic pipeline.
    """
    translated = translate_narration(script_text, target_lang)
    client = get_client()
    req_dict = normalize_request(
        {
            "input_text": translated,
            "voice_name": voice_name,
            "language_code": target_lang,
        }
    )
    # Build request object expected by google client
    from google.cloud import texttospeech
    request = texttospeech.SynthesizeSpeechRequest(
        input=texttospeech.SynthesisInput(ssml=translated) if "<speak>" in translated else texttospeech.SynthesisInput(text=translated),
        voice=texttospeech.VoiceSelectionParams(name=voice_name) if voice_name else None,
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3),
    )
    response = client.synthesize_speech(request=request)
    audio_bytes = response.audio_content
    print(f"Translated SSML length: {len(translated)} bytes")
    print(f"Synthesized audio bytes: {len(audio_bytes)}")
    return audio_bytes

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script_translate.py '<My narration here>' target_language [voice_name] [language_code]\")
        sys.exit(1)
    script = sys.argv[1]
    target = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else None
    lang = sys.argv[4] if len(sys.argv) > 4 else "en-US"
    audio = synthesize_translated(script, target, voice, lang)
    # Write to a local file for verification
    with open(f"translated_{target}.mp3", "wb") as f:
        f.write(audio)
    print("Audio saved as translated_{}.mp3".format(target))
