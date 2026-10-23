import asyncio
from speech_client import SpeechClient
from speech_models import AudioChunk, RecognitionConfig, RecognitionLanguage, LiveCaption

async def async_audio_chunk_source_for_partial_results():
    """Simulates an asynchronous source yielding audio chunks for partial results."""
    chunk_id = 0
    sentence_parts = [
        "Hello, this is a test.",
        "We are demonstrating streaming speech to text.",
        "With simulated partial results."
    ]

    for part in sentence_parts:
        await asyncio.sleep(0.5) # Simulate network delay or processing time
        chunk_data = part.encode() # Use the text as pseudo-audio data for simulation
        yield AudioChunk(chunk_id=chunk_id, content=chunk_data, sequence_number=chunk_id)
        chunk_id += 1
    yield AudioChunk(chunk_id=chunk_id, content=b"", sequence_number=chunk_id, is_last_chunk=True)

async def handle_streaming_recognition_events(language: RecognitionLanguage):
    speech_client = SpeechClient()
    config = RecognitionConfig(language=language)

    print(f"Handling streaming recognition events with {language.name} language...")
    async for audio_chunk in async_audio_chunk_source_for_partial_results():
        if audio_chunk.is_last_chunk:
            # Simulate a final result after the last chunk
            final_caption = LiveCaption(text="End of transcription.", language=language.value, is_partial=False)
            yield final_caption
            break
        
        # In a real streaming API, you would get partial results as they become available.
        # For OpenAI Whisper, we get a full transcription per chunk, so we'll treat them as interim for this demo.
        transcript_response = await speech_client.stream_audio_for_transcription(audio_chunk, config)
        if transcript_response.text:
            # Simulate an interim result
            interim_caption = LiveCaption(text=transcript_response.text, language=language.value, is_partial=True)
            yield interim_caption

async def main():
    async for caption_event in handle_streaming_recognition_events(RecognitionLanguage.ENGLISH):
        if caption_event.is_partial:
            print(f"Partial Result: {caption_event.text}")
        else:
            print(f"Final Result: {caption_event.text}")

if __name__ == "__main__":
    asyncio.run(main())
