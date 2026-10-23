import asyncio
import assemblyai as aai
from speech_client import get_speech_client

# A mock async generator to simulate streaming audio chunks from a source
async def mock_audio_chunk_generator():
    """
    Yields chunks of audio data. In a real application, this could be
    reading from a file, a network stream, etc.
    This example requires a dummy audio file named `test_audio.wav`.
    For this example, we will simulate empty chunks if the file is not found.
    """
    chunk_size = 512
    try:
        with open("test_audio.wav", "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data
                await asyncio.sleep(0.01) # Simulate real-time streaming
    except FileNotFoundError:
        print("Warning: 'test_audio.wav' not found. Yielding empty chunks.")
        for _ in range(10):
            yield b''
            await asyncio.sleep(0.1)


async def stream_audio_chunks():
    """
    Streams audio from an async generator of chunks to AssemblyAI for transcription.
    """
    transcriber = get_speech_client()
    
    async def on_data(transcript: aai.RealtimeTranscript):
        if transcript.text:
            print(transcript.text, end="\r")

    async def on_error(error: aai.RealtimeError):
        print(f"An error occurred: {error}")

    # The stream method takes an audio source
    streamer = transcriber.stream(
        on_data=on_data,
        on_error=on_error,
    )

    print("Streaming audio chunks...")
    await streamer.send_audio(mock_audio_chunk_generator())
    await streamer.close()


if __name__ == "__main__":
    # This script is designed to be run in an async context.
    # The main execution would be: asyncio.run(stream_audio_chunks())
    print("This script streams audio chunks using AssemblyAI.")

