"""
Summarize live meeting transcript chunks using OpenAI GPT chat completions.

Processes streaming meeting transcript segments and generates real-time
summarization using the OpenAI chat API.

Provider: OpenAI Chat Completions (GPT)
SDK: openai
Auth: OPENAI_API_KEY
"""

from __future__ import annotations

import os
from typing import AsyncGenerator, Optional

from openai import OpenAI

# OpenAI provider constants
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"
OPENAI_SUMMARY_TEMPERATURE = 0.3
OPENAI_SUMMARY_MAX_TOKENS = 500


def _get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for chat completions.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable must be set or api_key provided."
        )
    return OpenAI(api_key=key)


def summarize_transcript_chunk(
    transcript_text: str,
    previous_summary: str = "",
    model: str = OPENAI_SUMMARY_MODEL,
    api_key: Optional[str] = None,
) -> str:
    """
    Summarize a single meeting transcript chunk using OpenAI GPT.

    Args:
        transcript_text: Meeting transcript text to summarize.
        previous_summary: Optional previous summary for incremental updates.
        model: OpenAI model identifier (e.g., 'gpt-4o-mini', 'gpt-4o').
        api_key: OpenAI API key.

    Returns:
        Summarized meeting text.
    """
    client = _get_openai_client(api_key)

    system_prompt = (
        "You are a professional meeting summarizer. Provide concise, accurate "
        "summaries of meeting transcript excerpts. Focus on key decisions, "
        "action items, and important discussion points."
    )

    user_content = transcript_text
    if previous_summary:
        user_content = (
            f"Previous summary:\n{previous_summary}\n\n"
            f"New transcript excerpt:\n{transcript_text}\n\n"
            f"Provide an updated summary that incorporates the new information."
        )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=OPENAI_SUMMARY_TEMPERATURE,
        max_tokens=OPENAI_SUMMARY_MAX_TOKENS,
    )

    return response.choices[0].message.content.strip()


async def summarize_live_meeting(
    transcript_stream: AsyncGenerator[str, None],
    model: str = OPENAI_SUMMARY_MODEL,
    api_key: Optional[str] = None,
    incremental: bool = True,
) -> AsyncGenerator[dict, None]:
    """
    Summarize live meeting transcript chunks using OpenAI GPT.

    Consumes transcript text from an async generator and produces incremental
    or standalone summaries of meeting content via the OpenAI Chat Completions API.

    Args:
        transcript_stream: Async generator yielding meeting transcript text.
        model: OpenAI model identifier (e.g., 'gpt-4o-mini', 'gpt-4o').
        api_key: OpenAI API key.
        incremental: Whether to maintain and update a running summary.

    Yields:
        Dict with keys:
            - 'chunk_index': Sequential index of the processed chunk
            - 'summary': Generated summary text
            - 'chunk_text': Original transcript chunk
            - 'is_incremental': Whether this is an incremental summary update
            - 'model': Model used for summarization
    """
    client = _get_openai_client(api_key)
    accumulated_summary = ""
    chunk_index = 0

    system_prompt = (
        "You are a professional meeting summarizer. Provide concise, accurate "
        "summaries of meeting transcript excerpts. Focus on key decisions, "
        "action items, and important discussion points."
    )

    async for transcript_chunk in transcript_stream:
        if not transcript_chunk.strip():
            continue

        try:
            if incremental and accumulated_summary:
                user_content = (
                    f"Previous summary:\n{accumulated_summary}\n\n"
                    f"New transcript excerpt:\n{transcript_chunk}\n\n"
                    f"Provide an updated summary that incorporates the new information."
                )
            else:
                user_content = transcript_chunk

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=OPENAI_SUMMARY_TEMPERATURE,
                max_tokens=OPENAI_SUMMARY_MAX_TOKENS,
            )

            new_summary = response.choices[0].message.content.strip()
            accumulated_summary = new_summary

            yield {
                "chunk_index": chunk_index,
                "summary": new_summary,
                "chunk_text": transcript_chunk,
                "is_incremental": incremental and chunk_index > 0,
                "model": model,
            }

            chunk_index += 1

        except Exception as e:
            yield {
                "chunk_index": chunk_index,
                "summary": "",
                "chunk_text": transcript_chunk,
                "is_incremental": incremental and chunk_index > 0,
                "model": model,
                "error": str(e),
            }
            chunk_index += 1
