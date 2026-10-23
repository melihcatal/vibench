import asyncio
from typing import AsyncGenerator
from speech_client import SpeechClient
from speech_models import SpeechRecognitionChunk

async def stream_audio_chunks(audio_source: AsyncGenerator[bytes, None], language: str = "en") -> AsyncGenerator[SpeechRecognitionChunk, None]:
    speech_client = SpeechClient()
    print("Starting audio chunk streaming...")

    async for chunk in audio_source:
        if not chunk:
            continue

        try:
            transcript_result = await speech_client.stream_transcribe(chunk, language=language)
            yield SpeechRecognitionChunk(text=transcript_result.text, is_final=True) # OpenAI Whisper provides final results per API call
        except Exception as e:
            print(f"Error transcribing chunk: {e}")
            yield SpeechRecognitionChunk(text="", is_final=False)

async def simulated_async_audio_source(num_chunks: int = 3) -> AsyncGenerator[bytes, None]:
    simulated_chunks = [
        b"The quick brown fox jumps over the lazy dog.",
        b"Sphinx of black quartz, judge my vow.",
        b"How vexingly quick daft zebras jump."
    ]
    for i in range(min(num_chunks, len(simulated_chunks))):
        await asyncio.sleep(0.5) # Simulate async I/O
        print(f"Generating simulated chunk {i+1}...")
        yield simulated_chunks[i]

async def main():
    print("Demonstrating stream_chunks.py with simulated audio source.")
    async for transcript_chunk in stream_audio_chunks(simulated_async_audio_source()):
        print(f"Streamed Transcript: {transcript_chunk.text} (Final: {transcript_chunk.is_final})")

if __name__ == "__main__":
    asyncio.run(main())
