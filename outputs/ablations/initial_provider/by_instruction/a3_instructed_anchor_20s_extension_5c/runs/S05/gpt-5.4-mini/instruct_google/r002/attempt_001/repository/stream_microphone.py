import asyncio
from typing import AsyncIterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_streaming_config, load_speech_config, make_client
from speech_models import TranscriptSegment


async def microphone_audio_chunks() -> AsyncIterator[bytes]:
    while True:
        await asyncio.sleep(0.02)
        yield b""


async def stream_microphone() -> AsyncIterator[str]:
    cfg = load_speech_config()
    client = make_client()
    requests = [speech.StreamingRecognizeRequest(streaming_config=build_streaming_config(cfg))]
    async for chunk in microphone_audio_chunks():
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))
        for response in client.streaming_recognize(requests=requests):
            for result in response.results:
                if not result.alternatives:
                    continue
                yield result.alternatives[0].transcript
