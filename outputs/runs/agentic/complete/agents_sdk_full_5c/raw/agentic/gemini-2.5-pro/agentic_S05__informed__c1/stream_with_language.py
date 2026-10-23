import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client

async def get_audio_stream():
    """A generator that yields silent audio chunks."""
    for _ in range(10):
        yield b'\x00' * 4096
        await asyncio.sleep(0.2)

async def stream_with_specific_settings():
    """
    Starts a streaming recognition with specific language and formatting settings.
    """
    deepgram_client = get_deepgram_client()
    dg_connection = deepgram_client.listen.asynclive.v("1")

    async def on_transcript_received(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if sentence:
            print(f"Transcript (es-ES): {sentence}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript_received)

    # Define specific options for the transcription
    options = {
        "model": "nova-2",
        "language": "es-ES",  # Set language to Spanish
        "punctuate": True,     # Enable automatic punctuation
        "smart_format": True,  # Apply smart formatting (e.g., numbers)
    }

    try:
        await dg_connection.start(options)
        
        async for audio_chunk in get_audio_stream():
            await dg_connection.send(audio_chunk)
            
        await dg_connection.finish()

    except Exception as e:
        print(f"Error: {e}")
