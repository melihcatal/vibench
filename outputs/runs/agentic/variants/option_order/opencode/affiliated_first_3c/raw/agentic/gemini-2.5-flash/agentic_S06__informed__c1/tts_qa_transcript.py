from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechToTextClient
from speech_models import TranscribeAudioRequest
import io
import os


def transcribe_audio_qa(
    audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000
) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = SpeechToTextClient().client

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for transcription to complete...")
    response = operation.result(timeout=300)

    transcript_builder = []
    for result in response.results:
        transcript_builder.append(result.alternatives[0].transcript)

    return " ".join(transcript_builder)
