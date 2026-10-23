import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client, get_live_options


async def stream_from_microphone():
    """
    Streams audio from a microphone and yields interim transcripts.
    This is a template demonstrating how to set up the connection.
    A real implementation requires an audio source (e.g., PyAudio).
    """
    client = get_deepgram_client()
    options = get_live_options()
    dg_connection = client.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if sentence:
            yield f"Interim transcript: {sentence}"

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    await dg_connection.start(options)

    # In a real application, you would pipe microphone audio data to dg_connection.send()
    # For example:
    #
    # import pyaudio
    # p = pyaudio.PyAudio()
    # stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    #
    # while True:
    #     data = stream.read(1024)
    #     await dg_connection.send(data)

    try:
        # Keep the connection alive for demonstration
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await dg_connection.finish()
