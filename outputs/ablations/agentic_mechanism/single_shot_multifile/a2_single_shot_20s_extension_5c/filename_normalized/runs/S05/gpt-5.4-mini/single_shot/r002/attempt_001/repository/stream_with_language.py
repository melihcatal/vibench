import asyncio
from typing import AsyncIterator

from openai import AsyncOpenAI

from speech_client import build_openai_client, get_openai_model
from speech_models import StreamingTranscript, normalize_transcript


async def stream_with_language(language: str = "en", punctuation: bool = True) -> AsyncIterator[StreamingTranscript]:
    client: AsyncOpenAI = build_openai_client()
    model = get_openai_model()
    params = {
        "model": model,
        "file": ("audio.wav", b"", "audio/wav"),
        "response_format": "verbose_json",
        "language": language,
    }
    if punctuation:
        params["timestamp_granularities"] = ["word"]
    result = await client.audio.transcriptions.create(**params)
    text = normalize_transcript(getattr(result, "text", ""))
    if text:
        yield StreamingTranscript(text=text, is_final=True, language=getattr(result, "language", language))


async def main() -> None:
    async for item in stream_with_language("en"):
        print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
