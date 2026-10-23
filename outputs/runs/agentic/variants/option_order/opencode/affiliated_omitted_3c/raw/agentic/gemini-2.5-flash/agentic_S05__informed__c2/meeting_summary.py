import os
from typing import AsyncGenerator
from openai import AsyncOpenAI

from speech_models import TranscriptResult


async def summarize_text_chunk(text: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize the following meeting transcript chunk: {text}",
            },
        ],
    )
    return response.choices[0].message.content.strip()


async def meeting_summary(caption_stream: AsyncGenerator[TranscriptResult, None]):
    print("Summarizing live meeting transcript chunks...")
    full_transcript = []
    async for caption_result in caption_stream:
        if caption_result.text.strip():
            full_transcript.append(caption_result.text)
            if caption_result.is_final:
                # Summarize when a significant chunk or final result is available
                current_chunk_text = " ".join(full_transcript)
                if (
                    len(current_chunk_text.split()) > 20
                ):  # Summarize if chunk is reasonably long
                    summary = await summarize_text_chunk(current_chunk_text)
                    print(f"Meeting Summary: {summary}")
                    full_transcript = []  # Reset for next chunk
        yield caption_result
