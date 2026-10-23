"""
Summarize live meeting transcript chunks using OpenAI GPT-4.
Processes streaming transcript segments to generate real-time meeting summaries.

Provider: OpenAI Chat Completions API (GPT-4)
SDK: openai
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

import logging
from typing import Optional

from openai import OpenAI

from speech_models import FinalTranscriptResult

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a professional meeting summarization assistant. "
    "Summarize the provided meeting transcript concisely, highlighting key decisions, "
    "action items, and important discussion points. Use bullet points where appropriate."
)

DEFAULT_SUMMARY_PROMPT = "Provide a concise summary of the following meeting transcript:"


class MeetingSummarizer:
    """
    Summarizes live meeting transcripts using OpenAI GPT-4 API.

    Accumulates transcript chunks and generates summaries at configurable intervals.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.3,
    ):
        """
        Initialize the OpenAI meeting summarizer.

        Args:
            model: OpenAI model identifier (e.g., 'gpt-4o', 'gpt-4-turbo').
            system_prompt: System prompt for the summarization task.
            api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
            max_tokens: Maximum tokens for the summary output.
            temperature: Sampling temperature (0.0 to 1.0).
        """
        self.model = model
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.max_tokens = max_tokens
        self.temperature = temperature

        openai_key = api_key
        if not openai_key:
            import os
            openai_key = os.environ.get("OPENAI_API_KEY")

        self.client = OpenAI(api_key=openai_key)
        self._transcript_buffer: list[str] = []

    def add_transcript_chunk(self, result: FinalTranscriptResult) -> None:
        """
        Add a transcript chunk to the buffer.

        Args:
            result: FinalTranscriptResult to add.
        """
        if result.transcript:
            self._transcript_buffer.append(result.transcript)

    def add_text_chunk(self, text: str) -> None:
        """
        Add raw text to the transcript buffer.

        Args:
            text: Transcript text to add.
        """
        if text:
            self._transcript_buffer.append(text)

    def summarize(
        self,
        transcript: Optional[str] = None,
        custom_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate a summary using the OpenAI GPT-4 API.

        Args:
            transcript: Transcript text to summarize. If None, uses buffered transcript.
            custom_prompt: Optional custom prompt instead of the default.

        Returns:
            Generated summary text.
        """
        if transcript is None:
            transcript = " ".join(self._transcript_buffer).strip()

        if not transcript:
            return "No transcript content to summarize."

        prompt = custom_prompt or DEFAULT_SUMMARY_PROMPT

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{prompt}\n\n{transcript}"},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            summary = response.choices[0].message.content
            return summary if summary else "Unable to generate summary."
        except Exception as e:
            logger.error(f"OpenAI GPT-4 summarization error: {e}")
            return f"Error generating summary: {str(e)}"

    def summarize_and_clear(self, custom_prompt: Optional[str] = None) -> str:
        """
        Generate a summary from the buffered transcript and clear the buffer.

        Args:
            custom_prompt: Optional custom prompt.

        Returns:
            Generated summary text.
        """
        transcript = " ".join(self._transcript_buffer).strip()
        self._transcript_buffer.clear()
        return self.summarize(transcript, custom_prompt)

    def get_buffer_length(self) -> int:
        """Return the number of chunks in the transcript buffer."""
        return len(self._transcript_buffer)

    def get_buffer_text(self) -> str:
        """Return the full buffered transcript as a single string."""
        return " ".join(self._transcript_buffer).strip()


def create_summarizer(
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> MeetingSummarizer:
    """
    Factory function to create an OpenAI GPT-4 meeting summarizer.

    Args:
        model: OpenAI model identifier.
        api_key: OpenAI API key.
        system_prompt: Custom system prompt.

    Returns:
        Configured MeetingSummarizer instance.
    """
    return MeetingSummarizer(
        model=model,
        api_key=api_key,
        system_prompt=system_prompt,
    )
