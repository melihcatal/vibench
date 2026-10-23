from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents
from deepgram.options import LiveOptions
import logging
import asyncio

from speech_client import get_speech_client

load_dotenv()

async def stream_with_language_settings():
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    try:
        deepgram = get_speech_client()
        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript (es-ES): {sentence}")

        async def on_error(self, error, **kwargs):
            print(f"\n\nError: {error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        
        # Configure Deepgram options with specific language and formatting
        # For a list of languages, see: https://developers.deepgram.com/docs/languages
        options = LiveOptions(
            model="nova-2",
            language="es-ES",    # Set language to Spanish (Spain)
            punctuate=True,      # Enable automatic punctuation
            smart_format=True,   # Apply smart formatting (e.g., numbers, dates)
        )

        await dg_connection.start(options)
        
        logging.info("Microphone stream started with language='es-ES'. Press Ctrl+C to stop.")
        
        # Keep connection open
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Could not start microphone stream: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(stream_with_language_settings())
    except KeyboardInterrupt:
        logging.info("Stopping stream.")
