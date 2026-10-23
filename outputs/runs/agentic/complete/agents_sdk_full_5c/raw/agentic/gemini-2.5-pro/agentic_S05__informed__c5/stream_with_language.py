import asyncio
from deepgram import LiveOptions, LiveTranscriptionEvents

from speech_client import get_speech_client

async def stream_with_specific_language_and_punctuation():
    """
    Starts a streaming recognizer with Spanish language and punctuation enabled.
    """
    deepgram_client = get_speech_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcripción: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Configure the transcription options for Spanish with punctuation
        options = LiveOptions(
            model="nova-2",
            language="es",  # Set language to Spanish
            punctuate=True, # Enable automatic punctuation
        )
        
        await dg_connection.start(options)
        
        # In a real scenario, you would stream audio data here.
        # For this example, we'll simulate by waiting.
        print("Listening for Spanish speech... (simulated)")
        await asyncio.sleep(5)
        
        await dg_connection.finish()
        print("Finished.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(stream_with_specific_language_and_punctuation())
