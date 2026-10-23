"""Summarize live meeting transcript chunks using OpenAI API.

Uses the OpenAI Chat Completions API with gpt-4o-mini to generate summaries
of live meeting transcripts as they arrive.
"""

import os
from typing import List, Optional

import openai
from openai import OpenAI

from speech_models import clean_transcript_text

# OpenAI API base URL
OPENAI_API_BASE = "https://api.openai.com/v1"

# OpenAI model identifier for meeting summarization
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"

# Default system prompt for meeting summarization
DEFAULT_SUMMARY_SYSTEM_PROMPT = (
    "You are a professional meeting summarization assistant. "
    "Given a transcript of a live meeting, provide a concise summary "
    "highlighting key discussion points, decisions made, and action items. "
    "Use bullet points for clarity. Be objective and factual."
)


def get_openai_client() -> OpenAI:
    """Create an OpenAI API client.

    Returns:
        Configured OpenAI client using the OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set for OpenAI API access."
        )
    return OpenAI(api_key=api_key, base_url=OPENAI_API_BASE)


def summarize_transcript_chunk(
    transcript: str,
    system_prompt: Optional[str] = None,
    model: str = OPENAI_SUMMARY_MODEL,
    max_tokens: int = 512,
) -> str:
    """Summarize a single meeting transcript chunk using OpenAI gpt-4o-mini.

    Args:
        transcript: The meeting transcript text to summarize.
        system_prompt: Custom system prompt for the LLM.
        model: OpenAI model identifier (default: gpt-4o-mini).
        max_tokens: Maximum tokens in the response.

    Returns:
        Generated meeting summary text.
    """
    client = get_openai_client()
    cleaned = clean_transcript_text(transcript)

    if not cleaned:
        return ""

    system = system_prompt or DEFAULT_SUMMARY_SYSTEM_PROMPT

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": cleaned},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def summarize_meeting_chunks(
    transcript_chunks: List[str],
    system_prompt: Optional[str] = None,
    model: str = OPENAI_SUMMARY_MODEL,
    max_tokens: int = 1024,
) -> str:
    """Summarize a full meeting from multiple transcript chunks using OpenAI.

    Concatenates all chunks and generates a comprehensive meeting summary
    via the OpenAI gpt-4o-mini model.

    Args:
        transcript_chunks: List of transcript text chunks from the meeting.
        system_prompt: Custom system prompt for the LLM.
        model: OpenAI model identifier (default: gpt-4o-mini).
        max_tokens: Maximum tokens in the response.

    Returns:
        Comprehensive meeting summary text.
    """
    client = get_openai_client()
    combined = " ".join(clean_transcript_text(chunk) for chunk in transcript_chunks if chunk.strip())

    if not combined:
        return ""

    system = system_prompt or DEFAULT_SUMMARY_SYSTEM_PROMPT

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": combined},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def process_streaming_summary(
    transcript_events,
    chunk_window: int = 5,
    system_prompt: Optional[str] = None,
    model: str = OPENAI_SUMMARY_MODEL,
):
    """Process a stream of recognition events and yield periodic meeting summaries.

    Accumulates final transcripts and generates summaries every chunk_window
    final results using the OpenAI gpt-4o-mini model.

    Args:
        transcript_events: Iterator of (transcript, is_final, confidence) tuples.
        chunk_window: Number of final results before generating a summary.
        system_prompt: Custom system prompt.
        model: OpenAI model identifier (default: gpt-4o-mini).

    Yields:
        Tuples of (chunk_number, summary_text) for each generated summary.
    """
    buffer: List[str] = []
    chunk_count = 0

    for transcript, is_final, confidence in transcript_events:
        if not is_final:
            continue

        cleaned = clean_transcript_text(transcript)
        buffer.append(cleaned)

        if len(buffer) >= chunk_window:
            combined = " ".join(buffer)
            summary = summarize_transcript_chunk(
                combined,
                system_prompt=system_prompt,
                model=model,
            )
            chunk_count += 1
            yield chunk_count, summary
            buffer = []

    # Summarize any remaining buffer
    if buffer:
        combined = " ".join(buffer)
        summary = summarize_transcript_chunk(
            combined,
            system_prompt=system_prompt,
            model=model,
        )
        chunk_count += 1
        yield chunk_count, summary
