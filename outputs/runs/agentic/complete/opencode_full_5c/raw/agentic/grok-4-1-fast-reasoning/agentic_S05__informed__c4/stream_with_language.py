import asyncio
from typing import AsyncGenerator, AsyncIterable
from deepgram import LiveOptions, LiveTranscriptionEvents, LiveResult
from speech_client import get_stt_client
from speech_models import STTConfig


async def _send_audio(connection, audio_source: AsyncIterable[bytes]):
    try:
        async for chunk in audio_source:
            await connection.send(chunk)
    except:
        pass


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language: str = "en",
    punctuate: bool = True,
    model: str = "nova-2",
) -> AsyncGenerator[str, None]:
    config = STTConfig(model=model, language=language, punctuate=punctuate)
    client = get_stt_client()
    transcript_queue = asyncio.Queue()

    async def on_transcript(result: LiveResult, **kwargs):
        transcript = result.channel.alternatives[0].transcript or ""
        if transcript:
            await transcript_queue.put(transcript)

    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=True,
    )

    connection = client.listen.live.v("1").registerCallback(
        LiveTranscriptionEvents.Transcript, on_transcript
    )

    await connection.start(options)

    send_task = asyncio.create_task(_send_audio(connection, audio_source))

    try:
        while not send_task.done():
            try:
                transcript = await asyncio.wait_for(
                    transcript_queue.get(), timeout=0.05
                )
                yield transcript
            except asyncio.TimeoutError:
                pass
        await send_task
        while True:
            try:
                transcript = await asyncio.wait_for(transcript_queue.get(), timeout=0.5)
                yield transcript
            except asyncio.TimeoutError:
                break
    finally:
        await connection.finish()
