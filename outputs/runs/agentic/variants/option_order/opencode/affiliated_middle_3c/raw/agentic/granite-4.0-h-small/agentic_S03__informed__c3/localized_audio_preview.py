# [LATER-STEP] localized_audio_preview.py

import os
import tempfile
from typing import List, Dict

# Provider identification: DashScope CosyVoice TTS via dashscope SDK
from dashscope import audio
from dashscope import api_key

# Load API key from environment (demo placeholder)
api_key.set(api_key=os.getenv("DASHSCOPE_API_KEY"))


def synthesize_speech(
    translated_texts: List[str], language_code: str = "es"
) -> List[bytes]:
    """Generate spoken audio previews for translated strings.

    Uses DashScope CosyVoice TTS service.
    Returns raw WAV byte data for each text (or placeholder if unavailable).

    Args:
        translated_texts (List[str]): Texts that have already been translated.
        language_code (str): Target spoken language (e.g., 'es' for Spanish).

    Returns:
        List[bytes]: List of WAV audio bytes corresponding to each input.
    """
    results = []
    for txt in translated_texts:
        # CosyVoice TTS request; model is auto-selected per language
        response = audio.tts(text=txt, language=language_code)
        # response contains 'audio' field as base64; decode to bytes
        wav_bytes = response.audio.encode(
            "latin1"
        )  # typical base64 to bytes conversion
        results.append(wav_bytes)
    return results


# Mini demo (guarded by __main__)
if __name__ == "__main__":
    sample_texts = ["Hola, mundo!", "¡Gracias por comprar!"]
    audio_files = synthesize_speech(sample_texts, language_code="es")
    for i, wav in enumerate(audio_files):
        # Write to temporary files for demonstration (optional)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(wav)
            print(f"Wrote audio preview for entry {i} to {tmp.name}")
