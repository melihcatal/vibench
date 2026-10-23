from __future__ import annotations

from typing import Dict

from google.cloud import texttospeech

from model_client import load_config


VOICE_NAME = "en-US-Wavenet-D"


def generate_spoken_briefing(text: str, output_path: str = "briefing.mp3") -> Dict[str, str]:
    load_config()
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=VOICE_NAME)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(output_path, "wb") as f:
        f.write(response.audio_content)
    return {"provider": "google-cloud-texttospeech", "voice": VOICE_NAME, "output_path": output_path}
