from google.cloud import speech
import asyncio
from stream_chunks import stream_audio_chunks, dummy_async_audio_source

def handle_partial_results(response_generator):
    """
    Handles partial and final streaming recognition events from a Google Cloud Speech-to-Text response generator.
    """
    for response in response_generator:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"[FINAL] {transcript}")
            yield {"type": "final", "transcript": transcript}
        else:
            print(f"[PARTIAL] {transcript}")
            yield {"type": "partial", "transcript": transcript}

if __name__ == "__main__":
    async def main():
        audio_source = dummy_async_audio_source(num_chunks=7)
        response_gen = stream_audio_chunks(audio_source)
        async for event in handle_partial_results(response_gen):
            print(f"Handled Event: {event}")

    asyncio.run(main())
