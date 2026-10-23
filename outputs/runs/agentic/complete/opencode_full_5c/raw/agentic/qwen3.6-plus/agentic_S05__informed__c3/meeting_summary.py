from __future__ import annotations

import os
import logging
from collections.abc import AsyncGenerator

from mistralai import Mistral

from speech_models import TranscriptResult, StreamingEvent

logger = logging.getLogger(__name__)

MISTRAL_MODEL = "mistral-large-latest"


def create_mistral_client(api_key: str | None = None) -> Mistral:
    key = api_key or os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set")
    return Mistral(api_key=key)


async def summarize_meeting_chunks(
    source: AsyncGenerator[StreamingEvent, None],
    chunk_window: int = 10,
    model: str = MISTRAL_MODEL,
    client: Mistral | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    if client is None:
        client = create_mistral_client()

    buffer: list[str] = []
    summary_count = 0

    async for event in source:
        yield event

        if event.result is None or not event.result.text.strip():
            continue

        buffer.append(event.result.text.strip())

        if len(buffer) >= chunk_window:
            transcript_text = "\n".join(buffer)
            buffer.clear()

            try:
                summary = await _generate_summary(
                    client=client,
                    transcript=transcript_text,
                    model=model,
                    summary_index=summary_count,
                )
                summary_count += 1

                summary_result = TranscriptResult(
                    is_final=True,
                    text=summary,
                    language="en",
                    timestamp=event.result.timestamp,
                )

                yield StreamingEvent(
                    event_type="summary",
                    result=summary_result,
                    raw_payload={"summary_index": summary_count - 1},
                )
            except Exception as exc:
                logger.error("Mistral summary generation error: %s", exc)
                buffer.append(transcript_text)


async def _generate_summary(
    client: Mistral,
    transcript: str,
    model: str,
    summary_index: int,
) -> str:
    system_prompt = (
        "You are a meeting summarization assistant. "
        "Summarize the following meeting transcript excerpt concisely. "
        "Focus on key decisions, action items, and important discussion points. "
        "Keep the summary to 3-5 bullet points."
    )

    response = await client.chat.complete_async(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Meeting transcript excerpt (part {summary_index + 1}):\n\n{transcript}",
            },
        ],
        max_tokens=500,
        temperature=0.3,
    )

    if response and response.choices:
        return response.choices[0].message.content.strip()
    return ""


async def generate_final_meeting_summary(
    all_transcripts: list[str],
    model: str = MISTRAL_MODEL,
    client: Mistral | None = None,
) -> str:
    if client is None:
        client = create_mistral_client()

    full_transcript = "\n".join(all_transcripts)

    system_prompt = (
        "You are a professional meeting summarization assistant. "
        "Create a comprehensive summary of the full meeting transcript. "
        "Include: key topics discussed, decisions made, action items with owners, "
        "and any open questions. Format as a structured summary."
    )

    response = await client.chat.complete_async(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Full meeting transcript:\n\n{full_transcript}",
            },
        ],
        max_tokens=2000,
        temperature=0.3,
    )

    if response and response.choices:
        return response.choices[0].message.content.strip()
    return ""
