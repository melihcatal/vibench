import asyncio
import os
from dataclasses import dataclass
from typing import AsyncIterator, Optional

import google.cloud.speech_v1 as speech


@dataclass
class InterimTranscript:
    text: str
    is_final: bool


async def _microphone_audio_chunks(chunk_size: int = 4096) -> AsyncIterator[bytes]:
    import pyaudio

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            data = await asyncio.to_thread(stream.read, chunk_size, False)
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


async def stream_microphone(language_code: str = "en-US") -> AsyncIterator[InterimTranscript]:
    client = speech.SpeechAsyncClient()
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
        single_utterance=False,
    )

    async def request_stream() -> AsyncIterator[speech.StreamingRecognizeRequest]:
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in _microphone_audio_chunks():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(requests=request_stream())
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield InterimTranscript(text=result.alternatives[0].transcript, is_final=result.is_final)


async def main() -> None:
    async for transcript in stream_microphone():
        print(transcript.text)


if __name__ == "__main__":
    asyncio.run(main())
