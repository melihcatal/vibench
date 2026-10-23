from google.cloud import speech_v1p1beta1 as speech
import io
import os

def transcribe_audio(audio_bytes: bytes, audio_format: str, sample_rate_hertz: int = 16000) -> str:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3 if audio_format == "mp3" else \
                 speech.RecognitionConfig.AudioEncoding.OGG_OPUS if audio_format == "ogg_vorbis" else \
                 speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code="en-US", # Default language code
    )

    response = client.recognize(config=config, audio=audio)

    transcript = "".join([result.alternatives[0].transcript for result in response.results])
    return transcript
