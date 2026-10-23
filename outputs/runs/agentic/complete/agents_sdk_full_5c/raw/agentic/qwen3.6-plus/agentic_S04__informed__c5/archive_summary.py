"""
Summarize transcription results using OpenAI GPT via the Chat Completions API.

Takes a completed transcript and generates a concise summary using
the OpenAI gpt-4o-mini model.
"""

import os
from typing import List, Optional, Dict

from openai import OpenAI

from speech_models import TranscriptionResult, TranscriptionSegment


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client for GPT chat completions.

    Returns:
        Configured OpenAI client instance.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is required for OpenAI API access"
        )

    return OpenAI(api_key=api_key)


def build_transcript_prompt(
    transcript_text: str,
    system_prompt: Optional[str] = None,
    max_context_length: int = 100000,
) -> List[Dict[str, str]]:
    """
    Build the messages prompt for GPT summarization.

    Truncates the transcript if it exceeds the max context length to stay
    within the gpt-4o-mini token limits.

    Args:
        transcript_text: Full transcript text to summarize.
        system_prompt: Optional custom system prompt for the GPT model.
        max_context_length: Maximum characters of transcript to include.

    Returns:
        List of message dicts for the OpenAI Chat Completions API.
    """
    if system_prompt is None:
        system_prompt = (
            "You are a professional summarization assistant. "
            "You analyze meeting transcripts and produce concise, "
            "well-structured summaries that capture key discussion points, "
            "decisions, and action items."
        )

    if len(transcript_text) > max_context_length:
        truncated_text = transcript_text[:max_context_length] + "...[truncated]"
    else:
        truncated_text = transcript_text

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Please summarize the following meeting transcript.\n\n"
                f"Transcript:\n---\n{truncated_text}\n---\n\n"
                f"Provide a summary with:\n"
                f"1. Key topics discussed\n"
                f"2. Main decisions made\n"
                f"3. Action items and owners\n"
                f"4. Any follow-up items"
            ),
        },
    ]

    return messages


def summarize_transcript(
    transcript_result: TranscriptionResult,
    model: str = "gpt-4o-mini",
    max_tokens: int = 1024,
    temperature: float = 0.3,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Summarize a TranscriptionResult using the OpenAI GPT-4o-mini model.

    Sends the full transcript text to the OpenAI Chat Completions API
    and returns a structured summary.

    Args:
        transcript_result: The TranscriptionResult to summarize.
        model: OpenAI model to use (default: gpt-4o-mini).
        max_tokens: Maximum tokens in the generated summary.
        temperature: Sampling temperature for generation.
        system_prompt: Optional custom system prompt.

    Returns:
        Generated summary text from the OpenAI GPT model.

    Raises:
        openai.OpenAIError: If the API call fails.
    """
    client = get_openai_client()

    transcript_text = transcript_result.to_text()

    messages = build_transcript_prompt(
        transcript_text=transcript_text,
        system_prompt=system_prompt,
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary = response.choices[0].message.content
    return summary or ""


def summarize_with_speaker_context(
    transcript_result: TranscriptionResult,
    model: str = "gpt-4o-mini",
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> str:
    """
    Summarize a transcript with explicit speaker-aware context via GPT-4o-mini.

    Uses the speaker-labeled formatted text to help the OpenAI model
    identify who said what in the summary.

    Args:
        transcript_result: The TranscriptionResult with speaker information.
        model: OpenAI model to use (default: gpt-4o-mini).
        max_tokens: Maximum tokens in the summary.
        temperature: Sampling temperature.

    Returns:
        Speaker-aware summary text.
    """
    client = get_openai_client()

    transcript_text = transcript_result.to_segments_text(include_speaker=True)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a meeting summarization assistant. "
                "The transcript includes speaker labels in [Speaker] format. "
                "Use these labels to attribute statements to speakers in your summary. "
                "Focus on capturing who said what, key decisions, and action items."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Summarize this speaker-labeled transcript:\n\n"
                f"{transcript_text}"
            ),
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content or ""


def generate_archive_summary(
    transcript_result: TranscriptionResult,
    model: str = "gpt-4o-mini",
) -> Dict:
    """
    Generate a comprehensive archive summary with metadata for storage.

    Returns a structured dict suitable for archiving with the OpenAI GPT model,
    including title, executive summary, and key topics.

    Args:
        transcript_result: The transcript to archive.
        model: OpenAI model to use (default: gpt-4o-mini).

    Returns:
        Dictionary with title, summary, topics, action_items, and metadata.
    """
    client = get_openai_client()

    transcript_text = transcript_result.to_text()

    messages = [
        {
            "role": "system",
            "content": (
                "You are an archive assistant. Generate a structured summary "
                "of the meeting transcript in JSON-like format. Return only "
                "the structured data with: title, executive_summary, key_topics "
                "(list), action_items (list), and sentiment (positive/neutral/negative)."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Create an archive summary for this transcript:\n\n"
                f"{transcript_text}"
            ),
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.2,
    )

    summary_text = response.choices[0].message.content or ""

    return {
        "archive_summary": summary_text,
        "duration_ms": transcript_result.duration_ms,
        "segment_count": len(transcript_result.segments),
        "locale": transcript_result.locale,
    }
