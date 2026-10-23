from google.cloud import speech_v1p1beta1 as speech
import io
import os

def transcribe_audio(audio_bytes: bytes, sample_rate_hertz: int, language_code: str, project_id: str) -> str:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 from synthesis
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = "".join([result.alternatives[0].transcript for result in response.results])
    return transcript
