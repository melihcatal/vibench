from __future__ import annotations

from google.cloud import speech


def transcribe_tts_sample(audio_content: bytes, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)
