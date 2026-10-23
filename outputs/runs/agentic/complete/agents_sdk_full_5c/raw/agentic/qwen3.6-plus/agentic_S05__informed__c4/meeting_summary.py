"""Summarize live meeting transcript chunks using Anthropic Messages API (Claude)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Sequence

import anthropic

from speech_models import FinalTranscript


ANTHROPIC_API_ENV = "ANTHROPIC_API_KEY"

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
DEFAULT_MAX_TOKENS = 4096


@dataclass
class MeetingSummary:
    """A generated summary of meeting transcript chunks."""
    summary_text: str
    chunk_count: int
    total_transcript_length: int
    model_used: str
    raw_response: Any | None = None


def _get_anthropic_client() -> anthropic.Anthropic:
    """Create an Anthropic client using the API key from environment."""
    api_key = os.environ.get(ANTHROPIC_API_ENV)
    if not api_key:
        raise EnvironmentError(
            f"Environment variable {ANTHROPIC_API_ENV} is not set. "
            "Configure your Anthropic API key."
        )
    return anthropic.Anthropic(api_key=api_key)


SUMMARY_SYSTEM_PROMPT = """\
You are a professional meeting assistant. Your task is to produce concise, \
accurate summaries of meeting transcripts. Focus on:
- Key decisions made
- Action items and owners
- Open questions or follow-ups
- Important context or context changes

Be factual, neutral, and avoid speculation. Use bullet points for readability.\
"""


def _build_transcript_context(transcript_chunks: Sequence[str]) -> str:
    """Build a formatted context string from transcript chunks."""
    lines: list[str] = []
    for i, chunk in enumerate(transcript_chunks, start=1):
        lines.append(f"[Segment {i}]")
        lines.append(chunk.strip())
        lines.append("")
    return "\n".join(lines)


def summarize_meeting(
    transcript_chunks: Sequence[str],
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    system_prompt: str | None = None,
    temperature: float = 0.3,
) -> MeetingSummary:
    """
    Summarize a collection of meeting transcript chunks using Anthropic Claude.

    Parameters
    ----------
    transcript_chunks : Sequence[str]
        List of transcript text segments to summarize.
    model : str
        Anthropic model identifier (e.g. claude-3-5-sonnet-20241022).
    max_tokens : int
        Maximum tokens in the response.
    system_prompt : str | None
        Optional custom system prompt.
    temperature : float
        Sampling temperature.
    """
    client = _get_anthropic_client()
    context = _build_transcript_context(transcript_chunks)

    user_message = (
        f"Please summarize the following meeting transcript.\n\n"
        f"{context}\n\n"
        f"Provide a structured summary covering decisions, action items, "
        f"and open questions."
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt or SUMMARY_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    summary_text = "".join(
        block.text for block in message.content if hasattr(block, "text")
    )

    return MeetingSummary(
        summary_text=summary_text.strip(),
        chunk_count=len(transcript_chunks),
        total_transcript_length=sum(len(c) for c in transcript_chunks),
        model_used=model,
        raw_response=message,
    )


async def live_summarize_transcripts(
    transcripts: AsyncIterator[FinalTranscript],
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    window_size: int = 10,
    summary_interval: int = 5,
) -> AsyncIterator[MeetingSummary]:
    """
    Continuously summarize live meeting transcripts as they arrive.

    Maintains a rolling window of recent transcript chunks and periodically
    generates summaries using Anthropic Claude.

    Parameters
    ----------
    transcripts : AsyncIterator[FinalTranscript]
        Async iterator of final transcript segments.
    model : str
        Anthropic model identifier.
    max_tokens : int
        Maximum tokens per summary.
    window_size : int
        Maximum number of recent chunks to include in the summary context.
    summary_interval : int
        Generate a summary after this many new chunks arrive.
    """
    buffer: list[str] = []
    chunks_since_last_summary = 0

    async for transcript in transcripts:
        if transcript.text:
            buffer.append(transcript.text)
            if len(buffer) > window_size:
                buffer = buffer[-window_size:]

        chunks_since_last_summary += 1

        if chunks_since_last_summary >= summary_interval and len(buffer) >= 2:
            summary = summarize_meeting(
                transcript_chunks=buffer,
                model=model,
                max_tokens=max_tokens,
            )
            yield summary
            chunks_since_last_summary = 0
