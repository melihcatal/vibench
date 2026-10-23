from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents
from deepgram.options import LiveOptions
import logging
import asyncio

from speech_client import get_speech_client

load_dotenv()

async def stream_microphone():
    """Streams audio from the microphone and prints the transcript."""
    try:
        # Get the Deepgram client
        deepgram = get_speech_client()

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.asynclive.v("1")

        # Define event handlers
        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"transcript: {sentence}")

        async def on_error(self, error, **kwargs):
            print(f"\n\nError: {error}\n\n")

        # Register the event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # Configure Deepgram options for microphone streaming
        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            interim_results=False, # We only want final transcripts here
            encoding="linear16",
            sample_rate=16000,
        )

        # Start the connection
        await dg_connection.start(options, addons=None, endpoint="/v1/listen?multichannel=true")
        
        logging.info("Microphone stream started. Press Ctrl+C to stop.")
        
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)


    except Exception as e:
        print(f"Could not start microphone stream: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(stream_microphone())
    except KeyboardInterrupt:
        logging.info("Stopping microphone stream.")
