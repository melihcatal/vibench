import asyncio
from speech_client import get_speech_client
from deepgram import LiveOptions, LiveTranscriptionEvents

async def stream_with_settings():
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    deepgram_client = get_speech_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence):
                print(f"Transcripción: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Configure the streaming connection with Spanish language and punctuation
        options = LiveOptions(
            model="nova-2", 
            language="es",  # Set language to Spanish
            punctuate=True  # Enable automatic punctuation
        )
        
        print("Connecting to Deepgram with language='es' and punctuate=True...")
        # In a real application, you would start sending audio data here.
        await dg_connection.start(options)
        
        # Keep the connection open to receive results
        await asyncio.sleep(10)
        await dg_connection.finish()
        print("Connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # This script shows how to configure the streaming recognizer.
    # It will connect and wait for audio data.
    # asyncio.run(stream_with_settings())
    print("stream_with_language.py contains a runnable example. Please uncomment the last line to run.")
