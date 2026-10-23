import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options

async def stream_audio_chunks(audio_source: AsyncGenerator[bytes, None]):
    """
    Streams audio chunks from an async generator to Deepgram and prints transcripts.
    """
    deepgram_client = get_speech_client()
    options = get_live_options()

    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        # Define an event handler for the transcript
        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"Transcript: {transcript}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        await dg_connection.start(options)

        async for chunk in audio_source:
            if chunk:
                await dg_connection.send(chunk)

        # Finish the stream
        await dg_connection.finish()
        print("Stream finished.")

    except Exception as e:
        print(f"Error during streaming: {e}")
