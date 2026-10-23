import asyncio
import queue
import threading
from typing import AsyncGenerator, Optional

import pyaudio
from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    parse_deepgram_response,
    extract_interim_text,
    NormalizedTranscript,
)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000


async def stream_microphone(
    api_key: Optional[str] = None,
    language: str = "en",
    model: str = "nova-2",
    punctuate: bool = True,
    interim_results: bool = True,
) -> AsyncGenerator[NormalizedTranscript, None]:
    client = create_deepgram_client(api_key)
    options = build_live_options(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        sample_rate=RATE,
        channels=CHANNELS,
    )

    transcript_queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        is_final = result.is_final
        parsed = parse_deepgram_response(result.to_dict())
        normalized_list = [
            NormalizedTranscript(
                text=alt.transcript,
                confidence=alt.confidence,
                start_time=parsed.start,
                end_time=parsed.start + parsed.duration,
                is_final=is_final,
                words=alt.words,
                language=language,
            )
            for alt in parsed.alternatives
        ]
        for norm in normalized_list:
            asyncio.run_coroutine_threadsafe(transcript_queue.put(norm), loop)

    def on_error(self, error, **kwargs):
        pass

    dg_connection = client.listen.live.v("1")
    dg_connection.on("transcript", on_message)
    dg_connection.on("error", on_error)

    await asyncio.to_thread(dg_connection.start, options)

    audio_queue = queue.Queue()

    def _stream_audio():
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_queue.put(data)
        except Exception:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

    audio_thread = threading.Thread(target=_stream_audio, daemon=True)
    audio_thread.start()

    async def send_audio():
        while True:
            data = await asyncio.get_event_loop().run_in_executor(None, audio_queue.get)
            await asyncio.to_thread(dg_connection.send, data)

    send_task = asyncio.create_task(send_audio())

    try:
        while True:
            transcript = await transcript_queue.get()
            yield transcript
    finally:
        send_task.cancel()
        await asyncio.to_thread(dg_connection.finish)
