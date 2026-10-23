import asyncio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, RecognitionConfig, AudioEncoding, InterimResultsConfig

async def stream_audio_chunks(
    audio_chunk_generator,
    recognition_config: RecognitionConfig,
    interim_results_config: InterimResultsConfig
):
    client = get_speech_client()

    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding(recognition_config.encoding.value),
            sample_rate_hertz=recognition_config.sample_rate_hertz,
            language_code=recognition_config.language_code,
            enable_automatic_punctuation=recognition_config.enable_automatic_punctuation,
        ),
        interim_results=interim_results_config.interim_results,
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
