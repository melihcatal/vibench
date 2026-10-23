from google.cloud import speech_v1p1beta1 as speech
from typing import List, Dict

def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US") -> Dict:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    response = client.recognize(config=config, audio=audio)
    
    transcript = "".join(
        result.alternatives[0].transcript for result in response.results
    )
    confidence = sum(
        result.alternatives[0].confidence for result in response.results
    ) / len(response.results) if response.results else 0.0
    
    return {
        "transcript": transcript,
        "confidence": confidence,
        "language_code": language_code
    }