import asyncio
import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, SpeakOptions

async def handle_deepgram_results(deepgram_client: DeepgramClient, audio_source, language: str = "en-US"):
    """
    Connects to Deepgram to process audio from a source, handling partial and final results.

    Args:
        deepgram_client: An initialized DeepgramClient instance.
        audio_source: An async iterator that yields audio chunks (bytes).
        language: The language to use for transcription (e.g., "en-US").
    """
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")
        print("Successfully connected to Deepgram for partial results.")

        def on_open(self, open, **kwargs):
            print(f"Deepgram Connection Open: {open}")

        def on_close(self, close, **kwargs):
            print(f"Deepgram Connection Closed: {close}")

        def on_error(self, error, **kwargs):
            print(f"Deepgram Error: {error}")

        def on_transcript(self, result, **kwargs):
            if result.is_final:
                print(f"[FINAL] ", result.channel.alternatives[0].transcript)
            else:
                print(f"[PARTIAL] ", result.channel.alternatives[0].transcript)

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

        options = LiveOptions(
            punctuate=True,
            language=language,
            interim_results=True  # Enable interim results
        )
        await dg_connection.start(options)

        print("Sending audio from source...")
        async for chunk in audio_source:
            await dg_connection.send(chunk)

    except Exception as e:
        print(f"Error in handle_deepgram_results: {e}")
    finally:
        if 'dg_connection' in locals() and dg_connection.is_connecting:
            await dg_connection.finish()
        print("Result handling stream ended.")

# Dummy audio source for demonstration
async def dummy_audio_stream(num_chunks: int = 5, chunk_size: int = 1024):
    sample_text = "Hello this is a test of partial results from the Deepgram API."
    # In a real scenario, this would be actual audio data
    for i in range(num_chunks):
        # Simulate sending some audio that eventually forms the transcript
        yield sample_text.encode('utf-8') * (chunk_size // len(sample_text))
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    # This example requires DEEPGRAM_API_KEY environment variable to be set
    # deepgram_client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    # async def main():
    #     await handle_deepgram_results(deepgram_client, dummy_audio_stream())
    # asyncio.run(main())
    pass
