from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
import os
from dotenv import load_dotenv

from speech_client import get_speech_client

load_dotenv()

async def stream_from_microphone():
    """
    Streams audio from the microphone and prints the transcript.
    """
    try:
        deepgram_client = get_speech_client()

        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
        )
        await dg_connection.start(options)

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)
        microphone.start()

        input("Press Enter to stop recording...\n\n")

        microphone.finish()
        await dg_connection.finish()
        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return
