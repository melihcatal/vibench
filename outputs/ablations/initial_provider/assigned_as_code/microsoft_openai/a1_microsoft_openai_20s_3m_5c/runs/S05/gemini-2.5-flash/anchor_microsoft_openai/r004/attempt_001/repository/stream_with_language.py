from typing import Generator
from speech_client import AzureSpeechClient
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult

def stream_with_language(audio_chunks: Generator[bytes, None, None], language_code: str, enable_automatic_punctuation: bool, api_key: str, region: str, sample_rate_hz: int = 16000) -> Generator[SpeechRecognitionResult, None, None]:
    config = StreamingRecognitionConfig(
        language_code=language_code,
        sample_rate_hz=sample_rate_hz,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    client = AzureSpeechClient(api_key=api_key, region=region)
    yield from client.stream_recognize(audio_chunks, config)
