import asyncio
from google.cloud import speech


async def stream_audio_chunks(
    client: speech.SpeechClient,
    config: speech.RecognitionConfig,
    audio_chunks: list[bytes],
):
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def generate_requests():
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)
            await asyncio.sleep(0.01)  # Simulate real-time streaming

    responses = client.streaming_recognize(streaming_config, generate_requests())

    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript
            else:
                yield f"[Interim] {result.alternatives[0].transcript}"
