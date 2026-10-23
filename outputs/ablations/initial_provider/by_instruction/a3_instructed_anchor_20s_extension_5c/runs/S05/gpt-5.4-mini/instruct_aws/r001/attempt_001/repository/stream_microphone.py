import asyncio
from typing import AsyncIterator

from speech_client import build_transcribe_stream_client, load_streaming_speech_config
from speech_models import normalize_result_payload


async def _microphone_audio_chunks() -> AsyncIterator[bytes]:
    try:
        import sounddevice as sd
    except Exception as exc:
        raise RuntimeError("sounddevice is required for microphone streaming") from exc

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[bytes | None] = asyncio.Queue()

    def callback(indata, frames, time, status):
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    with sd.RawInputStream(samplerate=16000, channels=1, dtype="int16", callback=callback):
        while True:
            chunk = await queue.get()
            if chunk is None:
                return
            yield chunk


async def stream_microphone() -> AsyncIterator[str]:
    config = load_streaming_speech_config()
    client = build_transcribe_stream_client(config.region)
    stream = await client.start_stream_transcription(
        language_code=config.language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
    )
    async for audio_chunk in _microphone_audio_chunks():
        await stream.input_stream.send_audio_event(audio_chunk=audio_chunk)
        async for event in stream.output_stream:
            results = event.get("Transcript", {}).get("Results", [])
            for result in results:
                normalized = normalize_result_payload(result)
                if normalized.text:
                    yield normalized.text
