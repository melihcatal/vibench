from google.cloud import speech
from speech_client import get_speech_client


def stream_with_language(audio_stream, language_code="es-ES", enable_punctuation=True):
    """Starts a streaming recognizer with specific language and punctuation settings."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_stream
    )

    responses = client.streaming_recognize(streaming_config, requests)

    return responses
