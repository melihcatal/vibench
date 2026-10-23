import os
from google.cloud import speech
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio, AudioEncoding


def get_stt_client():
    return speech.SpeechClient()


def transcribe_tts_audio(
    audio_content: bytes,
    language_code: str = "en-US",
    sample_rate_hertz: int = 24000,
    encoding: AudioEncoding = AudioEncoding.MP3,
) -> str:
    client = get_stt_client()
    audio = RecognitionAudio(content=audio_content)
    config = RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return ""
    transcripts = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcripts)
