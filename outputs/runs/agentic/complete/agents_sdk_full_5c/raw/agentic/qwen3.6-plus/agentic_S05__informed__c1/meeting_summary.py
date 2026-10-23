"""
Summarize live meeting transcript chunks using OpenAI Chat Completions API.

Accumulates streaming meeting transcript chunks and generates summaries
using OpenAI's GPT-4 model via the OpenAI chat completions API.

Requires:
    pip install openai
"""

import os
from typing import List, Optional, Dict, Any

from openai import OpenAI

from speech_models import TranscriptChunk, TranscriptStatus


OPENAI_MODEL = "gpt-4o"


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client for chat completions.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.

    Raises:
        ValueError: If no API key is provided.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def format_transcript_for_summary(chunks: List[TranscriptChunk]) -> str:
    """Format transcript chunks into a readable meeting transcript.

    Args:
        chunks: List of TranscriptChunk objects from the meeting.

    Returns:
        Formatted transcript string suitable for summarization.
    """
    final_chunks = [c for c in chunks if c.is_final or c.status == TranscriptStatus.FINAL]
    if not final_chunks:
        final_chunks = chunks

    lines = []
    for i, chunk in enumerate(final_chunks):
        speaker_prefix = f"[Speaker {chunk.speaker}] " if chunk.speaker is not None else ""
        lines.append(f"{speaker_prefix}{chunk.normalize_text()}")

    return "\n".join(lines)


def summarize_meeting_transcript(
    chunks: List[TranscriptChunk],
    model: str = OPENAI_MODEL,
    summary_type: str = "comprehensive",
    max_tokens: int = 500,
    api_key: Optional[str] = None,
) -> str:
    """Summarize a meeting transcript using OpenAI GPT-4.

    Generates a comprehensive summary of the meeting transcript using
    the OpenAI chat completions API with the GPT-4o model.

    Args:
        chunks: List of TranscriptChunk objects from the meeting.
        model: OpenAI model identifier (e.g., 'gpt-4o', 'gpt-4-turbo').
        summary_type: Type of summary ('comprehensive', 'brief', 'action_items').
        max_tokens: Maximum tokens in the summary response.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Meeting summary string.
    """
    client = get_openai_client(api_key=api_key)
    transcript = format_transcript_for_summary(chunks)

    if summary_type == "comprehensive":
        system_prompt = (
            "You are an expert meeting summarizer. Provide a comprehensive "
            "summary of the meeting transcript including key discussion points, "
            "decisions made, and action items. Use bullet points for clarity."
        )
    elif summary_type == "brief":
        system_prompt = (
            "You are an expert meeting summarizer. Provide a brief, "
            "concise summary of the meeting transcript in 2-3 sentences."
        )
    elif summary_type == "action_items":
        system_prompt = (
            "You are an expert meeting summarizer. Extract and list all "
            "action items, decisions, and follow-up tasks from the meeting "
            "transcript. Format each item clearly with assigned owner if mentioned."
        )
    else:
        system_prompt = (
            "You are an expert meeting summarizer. Summarize the following "
            "meeting transcript."
        )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Meeting Transcript:\n\n{transcript}"},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    return summary


def summarize_meeting_stream(
    chunk_stream,
    model: str = OPENAI_MODEL,
    summary_interval: int = 10,
    summary_type: str = "comprehensive",
    api_key: Optional[str] = None,
):
    """Generate periodic summaries from a stream of meeting transcript chunks.

    Accumulates chunks and generates summaries at regular intervals using
    OpenAI's GPT-4 model.

    Args:
        chunk_stream: Async or sync iterator of TranscriptChunk objects.
        model: OpenAI model identifier.
        summary_interval: Number of chunks between summaries.
        summary_type: Type of summary to generate.
        api_key: OpenAI API key.

    Yields:
        Summary strings at each interval.
    """
    accumulated_chunks: List[TranscriptChunk] = []
    chunk_count = 0

    for chunk in chunk_stream:
        accumulated_chunks.append(chunk)
        chunk_count += 1

        if chunk_count >= summary_interval:
            summary = summarize_meeting_transcript(
                chunks=accumulated_chunks,
                model=model,
                summary_type=summary_type,
                api_key=api_key,
            )
            yield summary
            accumulated_chunks = []
            chunk_count = 0

    if accumulated_chunks:
        summary = summarize_meeting_transcript(
            chunks=accumulated_chunks,
            model=model,
            summary_type=summary_type,
            api_key=api_key,
        )
        yield summary


async def summarize_meeting_stream_async(
    chunk_stream,
    model: str = OPENAI_MODEL,
    summary_interval: int = 10,
    summary_type: str = "comprehensive",
    api_key: Optional[str] = None,
):
    """Async generator to summarize meeting transcript chunks using OpenAI.

    Args:
        chunk_stream: Async iterator of TranscriptChunk objects.
        model: OpenAI model identifier (e.g., 'gpt-4o').
        summary_interval: Number of chunks between summaries.
        summary_type: Type of summary to generate.
        api_key: OpenAI API key.

    Yields:
        Summary strings at each interval.
    """
    accumulated_chunks: List[TranscriptChunk] = []
    chunk_count = 0

    async for chunk in chunk_stream:
        accumulated_chunks.append(chunk)
        chunk_count += 1

        if chunk_count >= summary_interval:
            summary = summarize_meeting_transcript(
                chunks=accumulated_chunks,
                model=model,
                summary_type=summary_type,
                api_key=api_key,
            )
            yield summary
            accumulated_chunks = []
            chunk_count = 0

    if accumulated_chunks:
        summary = summarize_meeting_transcript(
            chunks=accumulated_chunks,
            model=model,
            summary_type=summary_type,
            api_key=api_key,
        )
        yield summary


def generate_meeting_notes(
    chunks: List[TranscriptChunk],
    model: str = OPENAI_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate structured meeting notes from transcript chunks.

    Uses OpenAI GPT-4o to extract structured meeting notes including
    summary, key decisions, action items, and participants.

    Args:
        chunks: List of TranscriptChunk objects.
        model: OpenAI model identifier.
        api_key: OpenAI API key.

    Returns:
        Dictionary with structured meeting notes.
    """
    client = get_openai_client(api_key=api_key)
    transcript = format_transcript_for_summary(chunks)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert meeting note-taker. Extract structured "
                    "meeting notes from the transcript. Return JSON with keys: "
                    "summary, key_decisions (list), action_items (list of "
                    "{task, owner, deadline}), participants (list)."
                ),
            },
            {"role": "user", "content": f"Meeting Transcript:\n\n{transcript}"},
        ],
        max_tokens=1000,
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    import json
    notes = json.loads(response.choices[0].message.content)
    return notes


if __name__ == "__main__":
    test_chunks = [
        TranscriptChunk(text="Welcome everyone to the meeting.", status=TranscriptStatus.FINAL, is_final=True, speaker=1),
        TranscriptChunk(text="Let's discuss the project timeline.", status=TranscriptStatus.FINAL, is_final=True, speaker=1),
        TranscriptChunk(text="I think we should finish by Friday.", status=TranscriptStatus.FINAL, is_final=True, speaker=2),
    ]

    print("Meeting summary would be generated here with a valid OPENAI_API_KEY")
