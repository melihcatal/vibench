from google.cloud import speech
from speech_client import get_speech_client


async def stream_chunks_from_source(async_audio_chunk_source, sample_rate_hz, language_code):
    client = get_speech_client()
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True
    )

    async def request_generator():
        async for chunk in async_audio_chunk_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=streaming_config, requests=request_generator())

    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}
