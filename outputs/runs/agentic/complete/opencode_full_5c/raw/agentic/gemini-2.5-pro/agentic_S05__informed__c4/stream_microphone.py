import asyncio
from deepgram import LiveTranscriptionEvents, LiveOptions, Microphone
from speech_client import get_speech_client
from speech_models import Caption


async def stream_microphone():
    """Streams microphone audio and yields interim transcripts."""
    transcript_queue = asyncio.Queue()
    client = get_speech_client()
    dg_connection = client.listen.live.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            await transcript_queue.put(
                Caption(text=transcript, is_final=result.is_final)
            )

    async def on_error(self, error, **kwargs):
        print(f"Error from Deepgram: {error}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    options = LiveOptions(model="nova-2", language="en-US", smart_format=True)
    await dg_connection.start(options)

    microphone = Microphone(dg_connection.send)
    microphone.start()

    try:
        while True:
            yield await transcript_queue.get()
    finally:
        microphone.finish()
        await dg_connection.finish()
