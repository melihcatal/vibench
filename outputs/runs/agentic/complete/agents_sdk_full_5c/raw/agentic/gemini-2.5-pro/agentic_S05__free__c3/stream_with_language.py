import asyncio
import base64
import assemblyai as aai
from speech_client import get_transcriber

# Simulate an asynchronous source of audio chunks
async def dummy_audio_source():
    # A silent 1-second WAV file chunk, encoded in base64
    silent_chunk_base64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhIAAAAAA="
    chunk_data = base64.b64decode(silent_chunk_base64)
    for _ in range(5):
        await asyncio.sleep(0.2)
        yield chunk_data

async def stream_with_custom_settings():
    """
    Starts a streaming recognition session with AssemblyAI using specific
    language and formatting settings.
    """
    # We get the base transcriber and then configure it
    transcriber = get_transcriber()

    final_transcripts = []

    def on_final_transcript(transcript: aai.RealtimeFinalTranscript):
        if transcript.text:
            print(f"Received final transcript: '{transcript.text}'")
            final_transcripts.append(transcript.text)

    transcriber.on_final_transcript = on_final_transcript

    # Configure the transcriber with specific settings before connecting
    config = aai.RealtimeTranscriptionConfig(
        sample_rate=16_000,
        language_code="es",  # Set language to Spanish
        punctuate=True,
    )
    
    await transcriber.connect_async(config=config)

    print("Recognizer started with language='es' and punctuation enabled.")

    async for chunk in dummy_audio_source():
        await transcriber.stream_async(chunk)

    await transcriber.close_async()
    
    return final_transcripts
