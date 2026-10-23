import asyncio
from typing import AsyncGenerator, Optional

import pyaudio
from deepgram import DeepgramClient

from speech_client import create_deepgram_client, get_streaming_options
from speech_models import (
    StreamingSpeechRequest,
    StreamingSpeechResponse,
    normalize_deepgram_result,
    normalize_transcript_for_downstream,
)

CHUNK_SIZE = 4096
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16


async def stream_with_language(
    language: str = "en",
    model: str = "nova-2",
    punctuation: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
    client: Optional[DeepgramClient] = None,
) -> AsyncGenerator[StreamingSpeechResponse, None]:
    if client is None:
        client = create_deepgram_client()

    request_config = StreamingSpeechRequest(
        language=language,
        model=model,
        punctuate=punctuation,
        interim_results=interim_results,
        smart_format=smart_format,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    options = get_streaming_options(
        language=language,
        punctuation=punctuation,
        interim_results=interim_results,
        smart_format=smart_format,
        model=model,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    dg_connection = client.listen.live.v("1")
    results_queue = asyncio.Queue()

    def _on_result(self_connection, result, **kwargs):
        results_queue.put_nowait(result)

    dg_connection.on("Results", _on_result)

    await dg_connection.start(options)

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    async def _send_audio():
        loop = asyncio.get_event_loop()
        while True:
            try:
                data = await loop.run_in_executor(
                    None, audio_stream.read, CHUNK_SIZE, False
                )
                await dg_connection.send(data)
            except Exception:
                break

    send_task = asyncio.create_task(_send_audio())

    try:
        while True:
            try:
                result = await asyncio.wait_for(results_queue.get(), timeout=2.0)
                response = normalize_deepgram_result(result)
                transcript_text = normalize_transcript_for_downstream(response)
                if transcript_text:
                    yield response
            except asyncio.TimeoutError:
                continue
    finally:
        send_task.cancel()
        try:
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
        except Exception:
            pass
        try:
            await dg_connection.finish()
        except Exception:
            pass
