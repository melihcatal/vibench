import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import create_streaming_recognition_config, create_recognition_config, ENCODING, SAMPLE_RATE_HERTZ, LANGUAGE_CODE


async def stream_audio_chunks(audio_chunk_source):
    client = get_speech_client()

    recognition_config = create_recognition_config(
        language_code=LANGUAGE_CODE,
        sample_rate_hertz=SAMPLE_RATE_HERTZ,
        enable_automatic_punctuation=True
    )
    streaming_config = create_streaming_recognition_config(recognition_config)

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunk_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(requests)

    # Note: client.streaming_recognize is a blocking call, 
    # but it yields responses as they become available. 
    # To make this truly async with async generators, 
    # an async client or wrapper would be needed. 
    # For this example, we iterate synchronously over the responses.
    for response in responses:
        yield response