from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
import os
from dotenv import load_dotenv

from speech_client import get_deepgram_client
from speech_models import TranscriptionResult

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_microphone():
    client = get_deepgram_client()
    dg_connection = client.listen.live.v("1")

    interim_results = []

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if result.is_final:
            interim_results.append(TranscriptionResult(text=sentence, is_final=True))
        elif len(sentence) > 0:
            interim_results.append(TranscriptionResult(text=sentence, is_final=False))

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        interim_results=True,
        smart_format=True,
    )

    await dg_connection.start(options)

    microphone = Microphone(dg_connection.send)
    microphone.start()

    # Process audio for a while, then stop.
    # In a real app, this would be based on user action.
    import asyncio

    await asyncio.sleep(10)

    microphone.finish()
    await dg_connection.finish()

    return interim_results


if __name__ == "__main__":
    import asyncio

    asyncio.run(stream_microphone())
