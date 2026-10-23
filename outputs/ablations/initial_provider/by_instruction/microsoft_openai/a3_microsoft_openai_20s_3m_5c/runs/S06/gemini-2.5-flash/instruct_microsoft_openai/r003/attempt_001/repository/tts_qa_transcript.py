import os
from google.cloud import speech_v1p1beta1 as speech
from speech_models import TranscriptionRequest

def transcribe_audio(request: TranscriptionRequest) -> str:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=request.audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 based on synthesis output
        sample_rate_hertz=16000,
        language_code=request.language_code,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)
