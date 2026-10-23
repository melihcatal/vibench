import asyncio
from typing import AsyncIterable, Callable
from deepgram import LiveOptions, LiveTranscriptionEvents, LiveResult
from speech_client import get_stt_client
from speech_models import STTConfig


async def transcribe_with_handlers(
    audio_source: AsyncIterable[bytes],
    config: STTConfig = STTConfig(),
    on_partial: Callable[[str], None] = lambda t: None,
    on_final: Callable[[str], None] = lambda t: None,
):
    client = get_stt_client()
    partial_queue = asyncio.Queue()
    final_queue = asyncio.Queue()

    async def on_transcript(result: LiveResult, **kwargs):
        transcript = result.channel.alternatives[0].transcript.strip()
        if not transcript:
            return
        if result.is_final:
            await final_queue.put(transcript)
        else:
            await partial_queue.put(transcript)

    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=True,
    )

    connection = client.listen.live.v("1").registerCallback(
        LiveTranscriptionEvents.Transcript, on_transcript
    )

    async def send_audio():
        async for chunk in audio_source:
            await connection.send(chunk)

    await connection.start(options)
    send_task = asyncio.create_task(send_audio())

    try:
        while not send_task.done():
            try:
                partial = await asyncio.wait_for(partial_queue.get(), timeout=0.1)
                on_partial(partial)
            except asyncio.TimeoutError:
                pass
            try:
                final_ = await asyncio.wait_for(final_queue.get(), timeout=0.1)
                on_final(final_)
            except asyncio.TimeoutError:
                pass
        await send_task
        while True:
            try:
                final_ = await asyncio.wait_for(final_queue.get(), timeout=0.1)
                on_final(final_)
            except asyncio.TimeoutError:
                break
    finally:
        await connection.finish()
