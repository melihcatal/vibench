import asyncio
from typing import AsyncGenerator, Callable, Awaitable, Optional

from deepgram import DeepgramClient

from speech_client import create_deepgram_client, get_streaming_options
from speech_models import (
    StreamingSpeechRequest,
    StreamingSpeechResponse,
    normalize_deepgram_result,
    normalize_transcript_for_downstream,
)


async def stream_chunks(
    audio_source: AsyncGenerator[bytes, None],
    client: Optional[DeepgramClient] = None,
    language: str = "en",
    model: str = "nova-2",
    punctuation: bool = True,
    interim_results: bool = True,
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
) -> AsyncGenerator[StreamingSpeechResponse, None]:
    if client is None:
        client = create_deepgram_client()

    request_config = StreamingSpeechRequest(
        language=language,
        model=model,
        punctuate=punctuation,
        interim_results=interim_results,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
    )

    options = get_streaming_options(
        language=language,
        punctuation=punctuation,
        interim_results=interim_results,
        model=model,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
    )

    dg_connection = client.listen.live.v("1")
    results_queue = asyncio.Queue()

    def _on_result(self_connection, result, **kwargs):
        results_queue.put_nowait(result)

    dg_connection.on("Results", _on_result)

    await dg_connection.start(options)

    async def _send_chunks():
        async for chunk in audio_source:
            await dg_connection.send(chunk)

    send_task = asyncio.create_task(_send_chunks())

    try:
        while True:
            try:
                result = await asyncio.wait_for(results_queue.get(), timeout=5.0)
                response = normalize_deepgram_result(result)
                transcript_text = normalize_transcript_for_downstream(response)
                if transcript_text:
                    yield response
            except asyncio.TimeoutError:
                break
    finally:
        send_task.cancel()
        try:
            await dg_connection.finish()
        except Exception:
            pass
