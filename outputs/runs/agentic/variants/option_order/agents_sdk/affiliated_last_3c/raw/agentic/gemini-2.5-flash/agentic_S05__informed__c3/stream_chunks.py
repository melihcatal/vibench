from google.cloud import speech
import asyncio

async def stream_audio_chunks(
    audio_chunks,
    sampling_rate: int = 16000,
    language_code: str = "en-US",
):
    """Streams audio chunks from an async source and yields transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in audio_chunks:
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield response
