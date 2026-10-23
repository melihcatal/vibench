from speech_client import get_speech_client
from speech_models import TranscriptionRequest
from google.cloud import speech_v1p1beta1 as speech

def submit_transcription(request: TranscriptionRequest) -> str:
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        request: A TranscriptionRequest object containing audio URI and configuration.

    Returns:
        The name of the long-running operation.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[request.config.encoding],
        sample_rate_hertz=request.config.sample_rate_hertz,
        language_code=request.config.language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name
