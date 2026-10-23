import os
from google.cloud import speech
from typing import Optional

def transcribe_tts_audio(audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 24000) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    
    response = client.recognize(config=config, audio=audio)
    
    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    
    return " ".join(transcripts)