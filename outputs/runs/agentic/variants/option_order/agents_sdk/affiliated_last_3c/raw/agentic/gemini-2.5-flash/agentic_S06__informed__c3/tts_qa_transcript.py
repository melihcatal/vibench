
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from speech_client import SpeechToTextClient

def transcribe_audio_for_qa(audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000) -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_content: The audio content (bytes) to transcribe.
        language_code: The language of the audio (e.g., "en-US").
        sample_rate_hertz: The sample rate of the audio.

    Returns:
        The transcribed text.
    """
    client_wrapper = SpeechToTextClient()
    client = client_wrapper.client

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, # Assumes LINEAR16 from TTS output
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return " ".join(transcripts)
