from __future__ import annotations

from typing import Optional

from google.cloud import speech_v1 as speech


def transcribe_tts_audio(audio_content: bytes, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(language_code=language_code, encoding=speech.RecognitionConfig.AudioEncoding.MP3)
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)


if __name__ == "__main__":
    print(transcribe_tts_audio(b""))
