from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_recognition_config, create_streaming_config

async def stream_chunks(audio_chunks_async_generator, sample_rate_hertz, language_code):
    client = get_speech_client()
    recognition_config = create_recognition_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    streaming_config = create_streaming_config(recognition_config, interim_results=True)

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=streaming_config, requests=request_generator())
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}
