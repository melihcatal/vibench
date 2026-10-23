from __future__ import annotations

from google.cloud import speech_v1


def transcribe_tts_sample(audio_bytes: bytes, language_code: str = "en-US") -> str:
    client = speech_v1.SpeechClient()
    audio = speech_v1.RecognitionAudio(content=audio_bytes)
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return ""
    return " ".join(result.alternatives[0].transcript for result in response.results if result.alternatives)
