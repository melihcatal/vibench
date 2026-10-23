import asyncio
import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

async def stream_audio_chunks(deepgram_client: DeepgramClient, audio_chunk_source, language: str = "en-US", punctuation: bool = True):
    """
    Streams audio chunks from an async source to Deepgram and yields transcripts.

    Args:
        deepgram_client: An initialized DeepgramClient instance.
        audio_chunk_source: An async iterator that yields audio chunks (bytes).
        language: The language to use for transcription (e.g., "en-US").
        punctuation: Whether to enable punctuation in the transcript.
    """
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")
        print("Successfully connected to Deepgram for chunk streaming.")

        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                yield transcript

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            punctuate=punctuation,
            language=language,
            interim_results=True
        )
        await dg_connection.start(options)

        print("Starting audio chunk stream...")
        async for chunk in audio_chunk_source:
            await dg_connection.send(chunk)

    except Exception as e:
        print(f"Error in stream_audio_chunks: {e}")
    finally:
        if 'dg_connection' in locals() and dg_connection.is_connecting:
            await dg_connection.finish()
        print("Audio chunk stream ended.")

# Example of an async audio chunk source (for demonstration)
async def get_dummy_audio_chunks(num_chunks: int = 10, chunk_size: int = 1024):
    for i in range(num_chunks):
        # Simulate sending a chunk of silent audio
        yield b'\x00' * chunk_size
        await asyncio.sleep(0.1) # Simulate real-time streaming

if __name__ == "__main__":
    # This example requires DEEPGRAM_API_KEY environment variable to be set
    # deepgram_client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    # async def main():
    #     print("Running dummy audio chunk stream...")
    #     async for transcript in stream_audio_chunks(deepgram_client, get_dummy_audio_chunks()):
    #         print(f"Chunk Transcript: {transcript}")
    # asyncio.run(main())
    pass
