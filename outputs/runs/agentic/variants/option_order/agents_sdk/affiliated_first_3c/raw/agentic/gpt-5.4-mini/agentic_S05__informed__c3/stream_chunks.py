from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import AzureSpeechStreamingClient, aiter_audio_chunks
from speech_models import TranscriptChunk


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[TranscriptChunk]:
    client = AzureSpeechStreamingClient()
    recognizer = client.recognizer()
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    recognizer.audio_config = audio_config

    async for chunk in aiter_audio_chunks(source):
        stream.write(chunk)
        yield TranscriptChunk(text=f"received {len(chunk)} bytes", is_final=False, metadata={"provider": "azure-speech"})

    stream.close()
    recognizer.stop_continuous_recognition_async().get()
