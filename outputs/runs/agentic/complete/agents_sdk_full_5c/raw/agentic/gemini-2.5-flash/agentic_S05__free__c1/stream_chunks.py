import asyncio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client, get_streaming_config

async def stream_audio_chunks(audio_chunk_source):
    client = get_speech_client()
    config = get_streaming_config()

    async def request_generator():
        async for chunk in audio_chunk_source():
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=config, requests=request_generator())
    for response in responses:
        for result in response.results:
            yield result.alternatives[0].transcript, result.is_final

if __name__ == 'main':
    # Example usage: simulate an async audio source
    async def simulated_audio_source():
        # Replace with your actual async audio source (e.g., from a network stream, file reader)
        chunks = [b"simulated audio chunk 1", b"simulated audio chunk 2"]
        for chunk in chunks:
            await asyncio.sleep(0.1) # Simulate async I/O
            yield chunk
        print("End of simulated audio.")

    async def main():
        print("Streaming audio chunks...")
        async for transcript, is_final in stream_audio_chunks(simulated_audio_source):
            if transcript:
                print(f"Transcript ({'Final' if is_final else 'Partial'}): {transcript}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping.")
