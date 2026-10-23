import asyncio
from typing import AsyncIterable, AsyncIterator

from google.cloud import speech_v1 as speech


async def stream_with_language(chunks: AsyncIterable[bytes], language_code: str = "en-US", enable_punctuation: bool = True, sample_rate_hertz: int = 16000) -> AsyncIterator[str]:
    client = speech.SpeechAsyncClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    responses = await client.streaming_recognize(streaming_config=streaming_config, requests=_requests(chunks))
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript


async def _requests(chunks: AsyncIterable[bytes]) -> AsyncIterator[speech.StreamingRecognizeRequest]:
    async for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)


async def main() -> None:
    async def empty_chunks() -> AsyncIterator[bytes]:
        if False:
            yield b""

    async for transcript in stream_with_language(empty_chunks()):
        print(transcript)


if __name__ == "__main__":
    asyncio.run(main())
