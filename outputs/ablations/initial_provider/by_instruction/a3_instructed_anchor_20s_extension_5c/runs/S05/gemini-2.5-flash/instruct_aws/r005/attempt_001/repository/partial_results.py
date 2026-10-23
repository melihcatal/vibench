import asyncio
from speech_models import TranscriptResult
from stream_chunks import stream_audio_chunks, simulated_audio_source

async def handle_streaming_recognition_events(audio_chunk_generator, language_code: str = "en-US"):
    print("Starting to handle streaming recognition events...")
    async for transcript_result in stream_audio_chunks(audio_chunk_generator, language_code=language_code):
        if transcript_result.is_partial:
            print(f"[PARTIAL RESULT] {transcript_result.transcript}")
        else:
            print(f"[FINAL RESULT]   {transcript_result.transcript}")

if __name__ == "__main__":
    async def main():
        print("Demonstrating handling of partial and final results using Google Cloud Speech-to-Text.")
        await handle_streaming_recognition_events(simulated_audio_source())
    asyncio.run(main())
