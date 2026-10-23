import asyncio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, RecognitionConfig, AudioEncoding, InterimResultsConfig

async def start_streaming_recognizer_with_settings(
    audio_chunk_generator,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
    encoding: AudioEncoding = AudioEncoding.LINEAR16,
    interim_results: bool = True,
):
    client = get_speech_client()

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding(encoding.value),
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunk_generator:
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    async for response in responses:
        yield response
