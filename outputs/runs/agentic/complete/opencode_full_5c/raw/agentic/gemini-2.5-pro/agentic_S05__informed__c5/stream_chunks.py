from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)
import asyncio

from speech_client import get_deepgram_client
from speech_models import TranscriptionResult


async def stream_audio_chunks(chunk_generator):
    client = get_deepgram_client()
    dg_connection = client.listen.live.v("1")

    transcripts = []

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        if result.is_final:
            transcripts.append(TranscriptionResult(text=sentence, is_final=True))
        else:
            transcripts.append(TranscriptionResult(text=sentence, is_final=False))

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )
    await dg_connection.start(options)

    async for chunk in chunk_generator:
        dg_connection.send(chunk)

    await dg_connection.finish()
    return transcripts


async def dummy_chunk_generator():
    # In a real application, this would be reading from a file,
    # a network stream, etc.
    for i in range(10):
        yield b"\x00" * 3200  # 0.1s of blank audio
        await asyncio.sleep(0.1)


if __name__ == "__main__":

    async def main():
        chunk_generator = dummy_chunk_generator()
        results = await stream_audio_chunks(chunk_generator)
        for result in results:
            print(result)

    asyncio.run(main())
