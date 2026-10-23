"""
Summarize transcription results using Anthropic Claude API.

Generates concise summaries of meeting transcripts using
Anthropic's Claude models via the official SDK.
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sys
from typing import Optional, Dict, Any, List

import anthropic
from anthropic import Anthropic


# Anthropic provider identifiers
PROVIDER = "Anthropic"
PROVIDER_MODEL = "claude-3-sonnet-20240229"
PROVIDER_API_HOST = "api.anthropic.com"


class TranscriptSummarizer:
    """Wrapper for Anthropic Claude transcript summarization."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = PROVIDER_MODEL,
    ):
        """
        Initialize Anthropic Claude client.

        Args:
            api_key: Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.
            model: Claude model identifier (default: claude-3-sonnet-20240229).
        """
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable must be set "
                "to use Anthropic Claude API"
            )
        self.client = Anthropic(api_key=key)
        self.model = model

    def summarize_transcript(
        self,
        transcript_text: str,
        summary_type: str = "meeting",
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """
        Generate a summary of a transcript using Claude.

        Args:
            transcript_text: Full transcript text to summarize.
            summary_type: Type of summary ('meeting', 'interview', 'general').
            max_tokens: Maximum tokens in summary response.

        Returns:
            Dict with summary text and metadata.
        """
        if summary_type == "meeting":
            system_prompt = (
                "You are an expert meeting summarizer. Provide a concise summary "
                "of the meeting transcript including: key decisions made, action items, "
                "and main discussion points. Use bullet points for clarity."
            )
        elif summary_type == "interview":
            system_prompt = (
                "You are an expert interview summarizer. Provide a concise summary "
                "of the interview including: key topics discussed, important statements, "
                "and notable quotes. Maintain neutrality."
            )
        else:
            system_prompt = (
                "You are an expert summarizer. Provide a concise, accurate summary "
                "of the following transcript. Highlight the main points and key information."
            )

        user_prompt = f"Please summarize the following transcript:\n\n{transcript_text}"

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

        summary_text = ""
        if message.content:
            for block in message.content:
                if hasattr(block, "text"):
                    summary_text += block.text

        return {
            "summary": summary_text,
            "summary_type": summary_type,
            "model": self.model,
            "provider": PROVIDER,
            "transcript_length": len(transcript_text),
            "summary_length": len(summary_text),
        }

    def extract_action_items(
        self,
        transcript_text: str,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """
        Extract action items from a meeting transcript.

        Args:
            transcript_text: Meeting transcript text.
            max_tokens: Maximum tokens in response.

        Returns:
            Dict with extracted action items.
        """
        prompt = (
            "Extract all action items, tasks, and commitments mentioned in "
            "the following meeting transcript. For each item, identify:\n"
            "- The action/task\n"
            "- Who is responsible (if mentioned)\n"
            "- Any deadlines (if mentioned)\n\n"
            f"Transcript:\n{transcript_text}"
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system="You are an expert at extracting action items from meeting transcripts.",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        action_items = ""
        if message.content:
            for block in message.content:
                if hasattr(block, "text"):
                    action_items += block.text

        return {
            "action_items": action_items,
            "model": self.model,
            "provider": PROVIDER,
        }


def summarize_transcription(
    transcript_text: str,
    summary_type: str = "meeting",
    api_key: Optional[str] = None,
    model: str = PROVIDER_MODEL,
) -> Dict[str, Any]:
    """
    Summarize a completed transcript using Anthropic Claude.

    Args:
        transcript_text: Full transcript text to summarize.
        summary_type: Type of summary ('meeting', 'interview', 'general').
        api_key: Optional Anthropic API key override.
        model: Claude model to use.

    Returns:
        Dict with summary and metadata.
    """
    summarizer = TranscriptSummarizer(api_key=api_key, model=model)
    return summarizer.summarize_transcript(
        transcript_text,
        summary_type=summary_type,
    )


def extract_archive_summary(
    transcript_text: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate an archive-ready summary of a transcript.

    Produces both a summary and extracted action items for archival.

    Args:
        transcript_text: Full transcript text.
        api_key: Optional Anthropic API key override.

    Returns:
        Dict with summary and action items.
    """
    summarizer = TranscriptSummarizer(api_key=api_key)
    summary = summarizer.summarize_transcript(transcript_text)
    actions = summarizer.extract_action_items(transcript_text)

    return {
        "summary": summary,
        "action_items": actions,
        "provider": PROVIDER,
    }


if __name__ == "__main__":
    # Example usage
    sample_transcript = """
    Meeting started at 10:00 AM. John welcomed everyone and introduced the agenda.
    Sarah presented the Q3 results, noting a 15% increase in revenue.
    Mike raised concerns about the delayed product launch.
    The team agreed to push the launch date by two weeks.
    Action items: Sarah will update the financial projections by Friday.
    Mike will coordinate with the engineering team on the new timeline.
    """

    result = summarize_transcription(sample_transcript)
    print(f"Summary:\n{result['summary']}")
