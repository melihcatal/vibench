import os

from google.cloud import speech


def transcribe_tts_audio(audio_content: bytes, language_code: str = None) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code or os.getenv("GCP_STT_LANGUAGE_CODE", "en-US"),
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join(
        result.alternatives[0].transcript
        for result in response.results
        if result.alternatives
    )
