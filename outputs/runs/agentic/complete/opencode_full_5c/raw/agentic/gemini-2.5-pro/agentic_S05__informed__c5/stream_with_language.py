from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)
import asyncio

from speech_client import get_deepgram_client
from speech_models import TranscriptionResult


async def stream_with_language_and_punctuation(audio_source, language="en-US"):
    client = get_deepgram_client()
    dg_connection = client.listen.live.v("1")

    transcripts = []

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if sentence:
            transcripts.append(
                TranscriptionResult(text=sentence, is_final=result.is_final)
            )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language=language,
        punctuate=True,
        smart_format=True,
    )

    await dg_connection.start(options)

    async for chunk in audio_source:
        dg_connection.send(chunk)

    await dg_connection.finish()
    return transcripts


async def dummy_audio_source():
    for _ in range(5):
        yield b"\x01" * 2048
        await asyncio.sleep(0.25)


if __name__ == "__main__":

    async def main():
        source = dummy_audio_source()
        # Example with Spanish
        results = await stream_with_language_and_punctuation(source, language="es")
        for res in results:
            print(f"Is Final: {res.is_final}, Text: {res.text}")

    asyncio.run(main())
