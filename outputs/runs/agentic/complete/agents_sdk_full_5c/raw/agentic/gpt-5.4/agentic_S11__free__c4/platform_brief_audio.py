from __future__ import annotations

from typing import Dict

from google.cloud import texttospeech


def platform_brief_audio(text: str, language_code: str = "en-US", voice_name: str = "en-US-Neural2-C") -> Dict[str, object]:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return {
        "provider": "google_cloud_text_to_speech",
        "voice_name": voice_name,
        "language_code": language_code,
        "audio_content": response.audio_content,
    }
