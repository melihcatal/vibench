"""Summarizes live meeting transcript chunks using OpenAI GPT-4o chat completions."""

import os
from typing import Optional
import openai
from speech_models import StreamingSpeechResult


OPENAI_API_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o"


SUMMARY_SYSTEM_PROMPT = """You are a meeting summarization assistant.
Summarize the provided meeting transcript concisely.
Focus on key decisions, action items, and important discussion points.
Use bullet points for clarity."""


class MeetingSummarizer:
    """
    Summarizes live meeting transcript chunks using OpenAI GPT-4o via openai SDK.

    Requires OPENAI_API_KEY environment variable.
    Model: gpt-4o (OpenAI Chat Completions API at api.openai.com).
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.3,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt or SUMMARY_SYSTEM_PROMPT
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = openai.OpenAI(api_key=key, base_url=OPENAI_API_URL)
        self.transcript_buffer: list[str] = []

    def add_chunk(self, result: StreamingSpeechResult) -> None:
        """Add a final transcript chunk to the buffer for summarization."""
        if result.is_final and result.transcript:
            self.transcript_buffer.append(result.transcript)

    def add_text(self, text: str) -> None:
        """Add raw text to the transcript buffer."""
        if text.strip():
            self.transcript_buffer.append(text.strip())

    def summarize(self, context: Optional[str] = None) -> str:
        """
        Generate a summary of the accumulated transcript using OpenAI GPT-4o.

        Uses openai.OpenAI chat.completions.create with model gpt-4o.
        Endpoint: api.openai.com/v1/chat/completions.
        """
        if not self.transcript_buffer:
            return ""

        transcript = "\n".join(self.transcript_buffer)
        user_content = transcript
        if context:
            user_content = f"{context}\n\nTranscript:\n{transcript}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response.choices[0].message.content or ""

    def summarize_incremental(
        self,
        new_text: str,
        previous_summary: Optional[str] = None,
    ) -> str:
        """
        Generate an updated summary incorporating new transcript content.

        Uses OpenAI GPT-4o model via openai SDK at api.openai.com.
        """
        system = (
            "You are a meeting summarization assistant. "
            "Merge the existing summary with new transcript content. "
            "Keep the result concise."
        )
        user_parts = []
        if previous_summary:
            user_parts.append(f"Existing summary:\n{previous_summary}")
        user_parts.append(f"New transcript:\n{new_text}")
        user_parts.append("Provide an updated summary incorporating the new content.")

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": "\n\n".join(user_parts)},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response.choices[0].message.content or ""

    def clear_buffer(self) -> None:
        """Clear the accumulated transcript buffer."""
        self.transcript_buffer.clear()


def create_summarizer(
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
) -> MeetingSummarizer:
    """Factory to create a MeetingSummarizer using OpenAI GPT-4o."""
    return MeetingSummarizer(model=model, max_tokens=max_tokens)
