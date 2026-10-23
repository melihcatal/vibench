from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)
import asyncio

from speech_client import get_deepgram_client
from speech_models import TranscriptionResult


async def handle_partial_and_final_results(audio_source):
    client = get_deepgram_client()
    dg_connection = client.listen.live.v("1")

    final_transcripts = []
    partial_transcripts = []

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return

        if result.is_final:
            final_transcripts.append(TranscriptionResult(text=sentence, is_final=True))
            print(f"Final: {sentence}")
        else:
            partial_transcripts.append(
                TranscriptionResult(text=sentence, is_final=False)
            )
            print(f"Partial: {sentence}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        interim_results=True,
    )
    await dg_connection.start(options)

    async for chunk in audio_source:
        dg_connection.send(chunk)

    await dg_connection.finish()

    return {"final": final_transcripts, "partial": partial_transcripts}


async def dummy_audio_source():
    for _ in range(5):
        yield b"\x01" * 1024
        await asyncio.sleep(0.2)


if __name__ == "__main__":
    asyncio.run(handle_partial_and_final_results(dummy_audio_source()))
