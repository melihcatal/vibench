import asyncio
import queue
import threading
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


async def stream_microphone(
    client: Optional[DeepgramClient] = None,
    language: str = "en",
    model: str = "nova-2",
    punctuation: bool = True,
    interim_results: bool = True,
) -> AsyncGenerator[StreamingSpeechResponse, None]:
    if client is None:
        client = create_deepgram_client()

    request_config = StreamingSpeechRequest(
        language=language,
        model=model,
        punctuate=punctuation,
        interim_results=interim_results,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    options = get_streaming_options(
        language=language,
        punctuation=punctuation,
        interim_results=interim_results,
        model=model,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    dg_connection = client.listen.live.v("1")

    audio_queue = queue.Queue()
    results_queue = queue.Queue()

    def _audio_capture():
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        try:
            while True:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                audio_queue.put(data)
        except Exception:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

    def _on_result(self_connection, result, **kwargs):
        results_queue.put(result)

    dg_connection.on("Results", _on_result)

    await dg_connection.start(options)

    capture_thread = threading.Thread(target=_audio_capture, daemon=True)
    capture_thread.start()

    async def _send_audio():
        loop = asyncio.get_event_loop()
        while True:
            try:
                data = await loop.run_in_executor(None, audio_queue.get, True, 1.0)
                await dg_connection.send(data)
            except queue.Empty:
                continue
            except Exception:
                break

    send_task = asyncio.create_task(_send_audio())

    try:
        while True:
            try:
                result = await asyncio.get_event_loop().run_in_executor(
                    None, results_queue.get, True, 2.0
                )
                response = normalize_deepgram_result(result)
                transcript_text = normalize_transcript_for_downstream(response)
                if transcript_text:
                    yield response
            except Exception:
                break
    finally:
        send_task.cancel()
        try:
            await dg_connection.finish()
        except Exception:
            pass
