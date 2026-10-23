import asyncio
import base64
from speech_client import get_transcriber
from speech_models import TranscriptResult

# Simulate an asynchronous source of audio chunks
async def dummy_audio_source():
    # A silent 1-second WAV file chunk, encoded in base64
    silent_chunk_base64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhIAAAAAA="
    chunk_data = base64.b64decode(silent_chunk_base64)
    for _ in range(5):
        await asyncio.sleep(0.2)
        yield chunk_data

async def handle_partial_and_final_results():
    """
    Demonstrates handling both partial (interim) and final transcription results
    from the AssemblyAI streaming service.
    """
    transcriber = get_transcriber()
    
    all_results = []

    def on_partial_transcript(partial_transcript):
        if partial_transcript.text:
            result = TranscriptResult(text=partial_transcript.text, is_final=False)
            print(f"Partial: {result.text}")
            all_results.append(result)

    def on_final_transcript(final_transcript):
        if final_transcript.text:
            result = TranscriptResult(text=final_transcript.text, is_final=True)
            print(f"Final:   {result.text}")
            all_results.append(result)

    transcriber.on_partial_transcript = on_partial_transcript
    transcriber.on_final_transcript = on_final_transcript
    
    await transcriber.connect_async()

    async for chunk in dummy_audio_source():
        await transcriber.stream_async(chunk)

    await transcriber.close_async()
    
    return all_results
