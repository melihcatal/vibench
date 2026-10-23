import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options

async def stream_with_specific_settings():
    """
    Starts a streaming recognizer with specific language (Spanish)
    and punctuation settings.
    """
    deepgram_client = get_speech_client()
    
    # Configure for Spanish language and enable punctuation
    options = get_live_options(
        language="es",
        punctuate=True,
        model="nova-2"
    )

    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"Transcripción en español: {transcript}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        await dg_connection.start(options)
        
        # Simulate sending Spanish audio data
        # In a real application, you would send microphone or file audio here.
        print("Connection started with language='es' and punctuate=True.")
        print("Waiting for audio... (simulated for 5 seconds)")
        await asyncio.sleep(5)

        await dg_connection.finish()

    except Exception as e:
        print(f"An error occurred: {e}")
