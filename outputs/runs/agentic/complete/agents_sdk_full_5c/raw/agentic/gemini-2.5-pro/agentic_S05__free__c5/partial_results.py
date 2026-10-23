import asyncio
from google.cloud.speech import StreamingRecognizeRequest
from speech_client import get_speech_client, get_streaming_config
from speech_models import CHUNK_SIZE, normalize_google_response

async def dummy_audio_source():
    """Yields silent audio chunks for demonstration."""
    for _ in range(30): # 3 seconds of silence
        await asyncio.sleep(0.1)
        yield bytes(CHUNK_SIZE * 2) # 16-bit audio

async def handle_streaming_results():
    """
    Sets up a stream to handle both partial and final recognition results
    and yields normalized TranscriptResult objects.
    """
    client = get_speech_client()
    # Enable interim_results
    streaming_config = get_streaming_config(interim_results=True)

    audio_generator = dummy_audio_source()
    requests = (StreamingRecognizeRequest(audio_content=chunk) async for chunk in audio_generator)

    # streaming_recognize returns an async generator
    responses = client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        normalized_results = normalize_google_response(response)
        for result in normalized_results:
            yield result

async def main():
    print("Processing stream for partial and final results...")
    result_handler = handle_streaming_results()
    async for result in result_handler:
        if result.is_final:
            print(f"FINAL: '{result.transcript}' (Confidence: {result.confidence:.2f})")
        else:
            print(f"PARTIAL: '{result.transcript}'")

if __name__ == "__main__":
    asyncio.run(main())
