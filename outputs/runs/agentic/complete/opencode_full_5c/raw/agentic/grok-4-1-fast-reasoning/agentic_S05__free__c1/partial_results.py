import asyncio
from typing import AsyncGenerator, AsyncIterable
from speech_models import Transcript


async def handle_partial_results(
    transcript_stream: AsyncIterable[Transcript],
) -> AsyncGenerator[Transcript, None]:
    current_partial = ""
    async for transcript in transcript_stream:
        text = transcript["text"].strip()
        if transcript["is_final"]:
            print(f"FINAL: {text}")
            current_partial = ""
        else:
            current_partial = text
            print(f"PARTIAL: {current_partial}")
        yield transcript
