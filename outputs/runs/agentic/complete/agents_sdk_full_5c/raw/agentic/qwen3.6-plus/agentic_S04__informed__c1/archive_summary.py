"""Summarize transcription results using Anthropic Messages API with Claude models."""

import os
from typing import Optional

import anthropic

from speech_models import TranscriptionResponse


ANTHROPIC_API_HOST = "api.anthropic.com"
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
DEFAULT_MAX_TOKENS = 1024


def create_anthropic_client(api_key: Optional[str] = None) -> anthropic.Anthropic:
    """Create an Anthropic client for the Messages API.

    Args:
        api_key: Anthropic API key; falls back to ANTHROPIC_API_KEY env var.

    Returns:
        Configured anthropic.Anthropic client instance.
    """
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
    return anthropic.Anthropic(api_key=api_key)


def summarize_transcript(
    response: TranscriptionResponse,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    api_key: Optional[str] = None,
) -> str:
    """Generate a summary of transcription results using Claude.

    Args:
        response: TranscriptionResponse to summarize.
        model: Anthropic model identifier (e.g., 'claude-3-5-sonnet-20241022').
        max_tokens: Maximum tokens for the summary.
        api_key: Optional Anthropic API key.

    Returns:
        Generated summary text.
    """
    client = create_anthropic_client(api_key)

    transcript_text = response.text
    if len(transcript_text) > 50000:
        transcript_text = transcript_text[:50000] + "... [truncated]"

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=(
            "You are an expert meeting summarizer. "
            "Provide a clear, structured summary of the transcript. "
            "Include key topics discussed, decisions made, and action items. "
            "Format with headings and bullet points."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summarize the following transcript (job_id: {response.job_id}):\n\n"
                    f"{transcript_text}"
                ),
            }
        ],
    )

    return message.content[0].text


def generate_archive_record(
    response: TranscriptionResponse,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> dict:
    """Generate a structured archive record with summary and metadata.

    Args:
        response: TranscriptionResponse to archive.
        model: Anthropic model identifier.
        api_key: Optional Anthropic API key.

    Returns:
        Dict with summary, metadata, and archival info.
    """
    summary = summarize_transcript(response, model=model, api_key=api_key)

    return {
        "job_id": response.job_id,
        "language": response.language,
        "audio_duration_ms": response.audio_duration_ms,
        "segment_count": len(response.segments),
        "word_count": len(response.text.split()),
        "summary": summary,
        "status": response.status,
    }


def extract_action_items(
    response: TranscriptionResponse,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> list:
    """Extract action items from a transcript using Claude.

    Args:
        response: TranscriptionResponse to analyze.
        model: Anthropic model identifier.
        api_key: Optional Anthropic API key.

    Returns:
        List of extracted action item strings.
    """
    client = create_anthropic_client(api_key)

    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=(
            "Extract action items from the transcript. "
            "Return a JSON array of strings, each representing one action item. "
            "Do not include any other text."
        ),
        messages=[
            {
                "role": "user",
                "content": f"Extract action items:\n\n{response.text}",
            }
        ],
    )

    import json
    try:
        result_text = message.content[0].text.strip()
        if result_text.startswith("```json"):
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif result_text.startswith("```"):
            result_text = result_text.split("```")[1].split("```")[0].strip()
        return json.loads(result_text)
    except (json.JSONDecodeError, IndexError):
        return [message.content[0].text.strip()]


if __name__ == "__main__":
    from speech_models import TranscriptionResponse, TranscriptSegment
    demo = TranscriptionResponse(
        job_id="archive-demo",
        text="Sample transcript for archival summary generation.",
        segments=[
            TranscriptSegment(text="We discussed the Q4 roadmap", start_ms=0, end_ms=3000),
            TranscriptSegment(text="and agreed on priorities", start_ms=3000, end_ms=5000),
        ],
    )
    print("Summarization requires ANTHROPIC_API_KEY to be set.")
