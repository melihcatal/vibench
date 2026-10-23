"""
Summarize live meeting transcript chunks using OpenAI Chat Completions API.

This module accumulates streaming transcript chunks and periodically sends
them to the OpenAI API (api.openai.com) using the chat.completions endpoint
with the gpt-4o-mini model to generate concise meeting summaries in real time.
"""

import asyncio
import json
import logging
import os
from typing import AsyncIterator, List, Optional

import httpx

logger = logging.getLogger(__name__)

OPENAI_API_ENDPOINT = "https://api.openai.com/v1"
OPENAI_CHAT_COMPLETIONS_URL = f"{OPENAI_API_ENDPOINT}/chat/completions"
OPENAI_MODEL_ID = "gpt-4o-mini"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

SUMMARIZE_SYSTEM_PROMPT = """\
You are a meeting summarization assistant. Given a transcript of a live meeting, \
produce a concise summary that captures:
- Key topics discussed
- Decisions made
- Action items with responsible parties (if mentioned)
- Open questions or follow-ups

Use bullet points and keep the summary brief and focused. \
Only summarize information present in the transcript."""


class MeetingSummarizer:
    """
    Generate live meeting summaries using the OpenAI Chat Completions API.

    Connects to api.openai.com and uses the gpt-4o-mini model to produce
    structured summaries from accumulated meeting transcript chunks.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = OPENAI_MODEL_ID,
        max_tokens: int = 512,
        temperature: float = 0.3,
        chunk_threshold: int = 500,
    ):
        """
        Initialize the meeting summarizer.

        Args:
            api_key: OpenAI API key for authentication.
            model: OpenAI model identifier (e.g., 'gpt-4o-mini').
            max_tokens: Maximum tokens in the summary response.
            temperature: Sampling temperature for generation.
            chunk_threshold: Minimum number of words before triggering summary.
        """
        self._api_key = api_key or os.environ.get(OPENAI_API_KEY_ENV, "")
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._chunk_threshold = chunk_threshold
        self._accumulated_text: List[str] = []
        self._summary_count: int = 0
        self._all_summaries: List[str] = []

        if not self._api_key:
            logger.warning(
                "%s not set; OpenAI API calls to %s will fail",
                OPENAI_API_KEY_ENV,
                OPENAI_API_ENDPOINT,
            )

        logger.info(
            "MeetingSummarizer initialized with model=%s via %s",
            model,
            OPENAI_API_ENDPOINT,
        )

    @property
    def accumulated_text(self) -> str:
        """Return all accumulated transcript text."""
        return " ".join(self._accumulated_text).strip()

    @property
    def all_summaries(self) -> List[str]:
        """Return all generated summaries."""
        return list(self._all_summaries)

    def add_transcript_chunk(self, text: str) -> None:
        """
        Add a new transcript chunk to the accumulator.

        Args:
            text: Transcript text from a speech recognition result.
        """
        if text and text.strip():
            self._accumulated_text.append(text.strip())

    def needs_summary(self) -> bool:
        """Check if enough text has accumulated to warrant a summary."""
        word_count = len(self.accumulated_text.split())
        return word_count >= self._chunk_threshold

    def reset_accumulator(self) -> str:
        """
        Clear the text accumulator and return the collected text.

        Returns:
            The accumulated text before clearing.
        """
        text = self.accumulated_text
        self._accumulated_text.clear()
        return text

    async def generate_summary(self, transcript_text: str) -> str:
        """
        Generate a meeting summary using the OpenAI Chat Completions API.

        Sends the transcript to api.openai.com using the gpt-4o-mini model.

        Args:
            transcript_text: Meeting transcript text to summarize.

        Returns:
            Generated summary string.
        """
        if not transcript_text.strip():
            return ""

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": f"Meeting transcript:\n\n{transcript_text}"},
            ],
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_CHAT_COMPLETIONS_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

        choices = result.get("choices", [])
        if not choices:
            logger.error("No choices returned from OpenAI API at %s", OPENAI_API_ENDPOINT)
            return ""

        summary_text = choices[0].get("message", {}).get("content", "").strip()
        self._summary_count += 1
        self._all_summaries.append(summary_text)

        logger.info(
            "Generated summary #%d via OpenAI %s (model=%s)",
            self._summary_count,
            OPENAI_API_ENDPOINT,
            self._model,
        )

        return summary_text


async def stream_meeting_summaries(
    transcript_stream: AsyncIterator[dict],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL_ID,
    chunk_threshold: int = 500,
    max_tokens: int = 512,
) -> AsyncIterator[dict]:
    """
    Consume a stream of transcript chunks and yield periodic meeting summaries.

    Accumulates transcript text and triggers summary generation when the
    word count threshold is reached using the OpenAI gpt-4o-mini model.

    Args:
        transcript_stream: Async iterator yielding dicts with 'text' and 'is_final' keys.
        api_key: OpenAI API key.
        model: OpenAI model identifier (default: gpt-4o-mini).
        chunk_threshold: Minimum word count before summarizing.
        max_tokens: Maximum tokens in each summary.

    Yields:
        dict: Summary result with text and metadata.
    """
    summarizer = MeetingSummarizer(
        api_key=api_key,
        model=model,
        chunk_threshold=chunk_threshold,
        max_tokens=max_tokens,
    )

    async for chunk in transcript_stream:
        text = chunk.get("text", "")
        is_final = chunk.get("is_final", False)

        if is_final and text.strip():
            summarizer.add_transcript_chunk(text)

        if summarizer.needs_summary():
            collected_text = summarizer.reset_accumulator()
            summary = await summarizer.generate_summary(collected_text)

            if summary:
                yield {
                    "summary": summary,
                    "chunk_index": summarizer._summary_count,
                    "model": model,
                    "source_endpoint": OPENAI_API_ENDPOINT,
                    "word_count": len(collected_text.split()),
                }
