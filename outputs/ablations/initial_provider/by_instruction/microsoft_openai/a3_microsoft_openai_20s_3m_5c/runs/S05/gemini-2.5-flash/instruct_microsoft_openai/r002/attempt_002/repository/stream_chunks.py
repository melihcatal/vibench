import asyncio
from speech_client import SpeechClient
from speech_models import AudioChunk, RecognitionConfig, RecognitionLanguage

async def async_audio_chunk_source():
    """Simulates an asynchronous source yielding audio chunks."""
    chunk_id = 0
    # In a real scenario, these would be actual audio bytes from a stream
    # For this example, we use placeholder bytes.
    for _ in range(5):
        await asyncio.sleep(1) # Simulate network delay or processing time
        chunk_data = b"Simulated audio chunk content " + str(chunk_id).encode()
        yield AudioChunk(chunk_id=chunk_id, content=chunk_data, sequence_number=chunk_id)
        chunk_id += 1
    yield AudioChunk(chunk_id=chunk_id, content=b"", sequence_number=chunk_id, is_last_chunk=True)

async def stream_audio_chunks(language: RecognitionLanguage):
    speech_client = SpeechClient()
    config = RecognitionConfig(language=language)

    print(f"Streaming audio chunks with {language.name} language...")
    async for audio_chunk in async_audio_chunk_source():
        if audio_chunk.is_last_chunk:
            print("End of audio stream.")
            break
        
        print(f"Processing audio chunk {audio_chunk.chunk_id}")
        transcript_response = await speech_client.stream_audio_for_transcription(audio_chunk, config)
        yield transcript_response.text

async def main():
    async for transcript in stream_audio_chunks(RecognitionLanguage.ENGLISH):
        if transcript:
            print(f"Transcript from chunk: {transcript}")

if __name__ == "__main__":
    asyncio.run(main())
