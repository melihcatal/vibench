import os
from typing import Optional, List

from openai import OpenAI

from speech_models import FinalTranscript


def load_openai_config() -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return {"api_key": api_key}


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    if api_key is None:
        config = load_openai_config()
        api_key = config["api_key"]
    return OpenAI(api_key=api_key)


SYSTEM_PROMPT = """You are a meeting summarization assistant. Given a transcript of a meeting conversation, produce a concise summary that captures:
1. Key topics discussed
2. Decisions made
3. Action items and owners
4. Open questions

Keep the summary structured and brief."""


async def summarize_meeting_chunks(
    transcript_chunks: List[FinalTranscript],
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o",
    max_tokens: int = 500,
) -> str:
    if client is None:
        client = create_openai_client()

    full_transcript = " ".join(chunk.text for chunk in transcript_chunks if chunk.text)

    if not full_transcript:
        return ""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Meeting transcript:\n\n{full_transcript}"},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    return summary


async def summarize_live_transcript_stream(
    transcript_stream,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o",
    chunk_size: int = 10,
    max_tokens: int = 500,
):
    if client is None:
        client = create_openai_client()

    chunks_buffer: List[FinalTranscript] = []

    async for item in transcript_stream:
        if isinstance(item, FinalTranscript):
            chunks_buffer.append(item)
        elif hasattr(item, "final") and item.final:
            chunks_buffer.append(item.final)

        if len(chunks_buffer) >= chunk_size:
            summary = await summarize_meeting_chunks(
                chunks_buffer, client=client, model=model, max_tokens=max_tokens
            )
            chunks_buffer.clear()
            yield summary
