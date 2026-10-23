from google.cloud import speech_v1p1beta1 as speech
from speech_models import SynthesisResponse
from typing import List


def transcribe_audio(audio_content: bytes, language_code: str = "en-US") -> List[str]:
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    
    response = client.recognize(config=config, audio=audio)
    transcripts = [result.alternatives[0].transcript for result in response.results]
    return transcripts


def verify_transcript(audio_response: SynthesisResponse, expected_text: str) -> bool:
    """Verify if the transcribed audio matches the expected text."""
    transcripts = transcribe_audio(audio_response.audio_content)
    return any(expected_text.lower() in transcript.lower() for transcript in transcripts)