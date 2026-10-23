import asyncio
from typing import AsyncGenerator

from deepgram import (
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

from speech_client import get_speech_client
from speech_models import StreamingTranscript


async def stream_microphone_transcription() -> AsyncGenerator[
    StreamingTranscript, None
]:
    client = get_speech_client()
    dg_connection = client.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return

        is_final = result.is_final
        confidence = result.channel.alternatives[0].confidence

        yield StreamingTranscript(
            text=sentence,
            is_final=is_final,
            confidence=confidence,
            words=result.channel.alternatives[0].words,
        )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        interim_results=True,
    )

    await dg_connection.start(options)

    microphone = Microphone(dg_connection.send)
    microphone.start()

    # The processing of results is handled by the on_message callback,
    # which is not directly awaited here. This example function's
    # primary role is to set up the stream. For a real application,
    # you would need a mechanism to collect and yield results from the callback.
    # For this structure, we'll simulate waiting for transcription.
    # In a real app, you'd manage the lifecycle of the connection and microphone.
    await asyncio.sleep(30)

    microphone.finish()
    await dg_connection.finish()
