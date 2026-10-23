import asyncio
import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

async def stream_microphone():
    """
    Streams audio from the microphone and prints the transcript.
    This function sets up a streaming connection to Deepgram and uses a local
    microphone as the audio source.
    """
    try:
        # Requires DEEPGRAM_API_KEY to be set as an environment variable
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"speaker: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
        )

        await dg_connection.start(options)

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)
        microphone.start()

        # Keep the connection open while the microphone is running
        print("Microphone stream started. Press Ctrl+C to stop.")
        await asyncio.sleep(30) # Stream for 30 seconds as an example

        # Stop the microphone and close the connection
        microphone.finish()
        await dg_connection.finish()
        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    # To run this, you'll need to install pyaudio:
    # pip install pyaudio
    # And have the portaudio library installed on your system.
    # asyncio.run(stream_microphone())
    print("stream_microphone.py contains a runnable example. Please uncomment the last line to run.")
