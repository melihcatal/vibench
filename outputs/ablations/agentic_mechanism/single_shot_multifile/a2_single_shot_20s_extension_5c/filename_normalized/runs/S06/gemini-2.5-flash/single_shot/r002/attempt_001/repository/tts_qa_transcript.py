import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums as speech_enums
from typing import List

def transcribe_audio_for_qa(
    audio_content: bytes,
    language_code: str = "en-US",
    sample_rate_hertz: int = 24000,
    encoding: speech_enums.RecognitionConfig.AudioEncoding = speech_enums.RecognitionConfig.AudioEncoding.MP3
) -> List[str]:
    """
    Transcribes synthesized audio samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        model="default" # For general audio transcription
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return transcripts
