import asyncio
from typing import AsyncGenerator, Optional, Union

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import parse_deepgram_response, StreamingTranscriptResponse


async def stream_chunks(
    audio_source: AsyncGenerator[bytes, None],
    api_key: Optional[str] = None,
    language: str = "en",
    model: str = "nova-2",
    punctuate: bool = True,
    interim_results: bool = True,
    sample_rate: int = 16000,
    channels: int = 1,
) -> AsyncGenerator[StreamingTranscriptResponse, None]:
    client = create_deepgram_client(api_key)
    options = build_live_options(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        sample_rate=sample_rate,
        channels=channels,
    )

    result_queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def on_transcript(self, result, **kwargs):
        raw = result.to_dict()
        parsed = parse_deepgram_response(raw)
        asyncio.run_coroutine_threadsafe(result_queue.put(parsed), loop)

    def on_error(self, error, **kwargs):
        pass

    dg_connection = client.listen.live.v("1")
    dg_connection.on("transcript", on_transcript)
    dg_connection.on("error", on_error)

    await asyncio.to_thread(dg_connection.start, options)

    async def send_chunks():
        async for chunk in audio_source:
            await asyncio.to_thread(dg_connection.send, chunk)

    send_task = asyncio.create_task(send_chunks())

    try:
        while True:
            response = await result_queue.get()
            yield response
            if response.is_final and response.speech_final:
                break
    finally:
        send_task.cancel()
        await asyncio.to_thread(dg_connection.finish)


async def chunked_file_source(
    file_path: str, chunk_size: int = 8192
) -> AsyncGenerator[bytes, None]:
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


async def chunked_buffer_source(
    buffer: bytes, chunk_size: int = 8192
) -> AsyncGenerator[bytes, None]:
    for i in range(0, len(buffer), chunk_size):
        yield buffer[i : i + chunk_size]
