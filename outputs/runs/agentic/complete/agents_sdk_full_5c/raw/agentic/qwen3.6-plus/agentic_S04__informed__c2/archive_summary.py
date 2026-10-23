"""
[LATER-STEP] Summarize transcription results via Anthropic Claude API.

Uses the Anthropic Messages API with the Claude model to generate
concise meeting summaries from AssemblyAI transcript output.
Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-5-sonnet-20241022
"""

import os
from typing import List, Optional, Dict, Any

from anthropic import Anthropic, AnthropicError

from speech_models import TranscriptResponse


ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def get_anthropic_client(api_key: Optional[str] = None) -> Anthropic:
    """
    Create and return an Anthropic client.

    Args:
        api_key: Optional Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.

    Returns:
        Configured anthropic.Anthropic instance.

    Raises:
        ValueError: If no API key is found.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError(
            "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or pass api_key."
        )
    return Anthropic(api_key=key)


def summarize_transcript(
    transcript: TranscriptResponse,
    summary_type: str = "detailed",
    model: str = ANTHROPIC_MODEL,
    max_tokens: int = 1024,
    api_key: Optional[str] = None,
    language: str = "en",
) -> Dict[str, Any]:
    """
    Generate a summary of the transcript using Anthropic Claude.

    Args:
        transcript: Normalized TranscriptResponse with full_text.
        summary_type: Type of summary: 'detailed', 'brief', 'action_items', or 'bullet_points'.
        model: Anthropic model identifier (default: claude-3-5-sonnet-20241022).
        max_tokens: Maximum tokens for the summary response.
        api_key: Anthropic API key.
        language: Language for the summary.

    Returns:
        Dictionary with summary text, type, model used, and transcript metadata.

    Raises:
        AnthropicError: If the API call fails.
    """
    client = get_anthropic_client(api_key)

    prompt_system = _build_system_prompt(summary_type, language)
    prompt_user = _build_user_prompt(transcript)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=prompt_system,
        messages=[
            {
                "role": "user",
                "content": prompt_user,
            }
        ],
    )

    summary_text = ""
    if message.content:
        for block in message.content:
            if hasattr(block, "text"):
                summary_text += block.text

    return {
        "transcript_id": transcript.transcript_id,
        "summary_type": summary_type,
        "summary": summary_text,
        "model": model,
        "language": language,
        "audio_duration_ms": transcript.duration_ms,
        "original_text_length": len(transcript.full_text),
    }


def _build_system_prompt(summary_type: str, language: str) -> str:
    """
    Build the system prompt for Anthropic Claude based on summary type.

    Args:
        summary_type: Type of summary to generate.
        language: Target language.

    Returns:
        System prompt string.
    """
    base = "You are an expert meeting analyst. You analyze meeting transcripts and produce clear, accurate summaries."

    type_prompts = {
        "detailed": (
            "Produce a comprehensive summary covering all major discussion points, "
            "decisions made, and key themes. Include relevant context and nuances. "
            "Structure with clear headings and sections."
        ),
        "brief": (
            "Produce a concise executive summary in 3-5 sentences covering the "
            "most important points and outcomes of the meeting."
        ),
        "action_items": (
            "Extract all action items, decisions, and follow-up tasks from the transcript. "
            "List each with the responsible party (if mentioned) and any deadlines. "
            "Format as a structured list."
        ),
        "bullet_points": (
            "Produce a bullet-point summary of the key discussion topics and outcomes. "
            "Each bullet should be self-contained and cover one distinct point."
        ),
    }

    type_prompt = type_prompts.get(summary_type, type_prompts["detailed"])

    return f"{base}\n\n{type_prompt}\n\nRespond in {language}."


def _build_user_prompt(transcript: TranscriptResponse) -> str:
    """
    Build the user prompt containing transcript text for Claude.

    Args:
        transcript: Normalized TranscriptResponse.

    Returns:
        User prompt string with transcript content.
    """
    parts = []

    if transcript.utterances:
        parts.append("Meeting transcript with speaker labels:")
        for utterance in transcript.utterances:
            speaker = utterance.speaker or "Unknown"
            parts.append(f"[{speaker}]: {utterance.text}")
    else:
        parts.append("Meeting transcript:")
        parts.append(transcript.full_text)

    return "\n".join(parts)


def summarize_by_speaker(
    transcript: TranscriptResponse,
    model: str = ANTHROPIC_MODEL,
    max_tokens: int = 512,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate per-speaker summaries using Anthropic Claude.

    Args:
        transcript: Normalized TranscriptResponse.
        model: Anthropic model identifier.
        max_tokens: Maximum tokens per speaker summary.
        api_key: Anthropic API key.

    Returns:
        Dictionary mapping speaker IDs to their summaries.
    """
    client = get_anthropic_client(api_key)
    speakers = transcript.get_speakers()

    summaries = {}
    for speaker in speakers:
        speaker_utterances = transcript.get_utterances_by_speaker(speaker)
        speaker_text = "\n".join([u.text for u in speaker_utterances])

        if not speaker_text.strip():
            summaries[speaker] = "No content to summarize."
            continue

        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system="Summarize what this speaker contributed to the meeting. Focus on their key points, opinions expressed, and any commitments made.",
            messages=[
                {
                    "role": "user",
                    "content": f"Speaker {speaker} said:\n\n{speaker_text}",
                }
            ],
        )

        summary_text = ""
        if message.content:
            for block in message.content:
                if hasattr(block, "text"):
                    summary_text += block.text

        summaries[speaker] = summary_text

    return {
        "transcript_id": transcript.transcript_id,
        "speaker_summaries": summaries,
        "model": model,
    }


def generate_archive_metadata(
    transcript: TranscriptResponse,
    summary_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate archive metadata combining transcript info and LLM summary.

    Args:
        transcript: Normalized TranscriptResponse.
        summary_result: Summary output from summarize_transcript().

    Returns:
        Archive metadata dictionary suitable for storage.
    """
    return {
        "archive_id": transcript.transcript_id,
        "audio_url": transcript.audio_url,
        "transcript_length": len(transcript.full_text),
        "audio_duration_ms": transcript.duration_ms,
        "language": transcript.language_code,
        "speaker_count": len(transcript.get_speakers()),
        "summary": summary_result.get("summary", ""),
        "summary_type": summary_result.get("summary_type", "detailed"),
        "summarization_model": summary_result.get("model", ANTHROPIC_MODEL),
        "status": transcript.status,
    }


def main():
    """CLI entry point for summarizing a transcript."""
    import argparse

    parser = argparse.ArgumentParser(description="Summarize transcript with Anthropic Claude")
    parser.add_argument("transcript_id", help="Transcript ID to summarize")
    parser.add_argument(
        "--type",
        choices=["detailed", "brief", "action_items", "bullet_points"],
        default="detailed",
        help="Summary type",
    )
    parser.add_argument("--language", default="en", help="Summary language")
    parser.add_argument(
        "--model",
        default=ANTHROPIC_MODEL,
        help=f"Anthropic model (default: {ANTHROPIC_MODEL})",
    )
    parser.add_argument("--by-speaker", action="store_true", help="Generate per-speaker summaries")

    args = parser.parse_args()

    from poll_transcription import poll_transcription

    transcript = poll_transcription(args.transcript_id)

    if args.by_speaker:
        results = summarize_by_speaker(
            transcript=transcript,
            model=args.model,
        )
        print("=== Per-Speaker Summaries ===")
        for speaker, summary in results["speaker_summaries"].items():
            print(f"\n--- Speaker {speaker} ---")
            print(summary)
    else:
        results = summarize_transcript(
            transcript=transcript,
            summary_type=args.type,
            model=args.model,
            language=args.language,
        )
        print(f"=== Transcript Summary ({results['summary_type']}) ===")
        print(f"Model: {results['model']}")
        print(f"\n{results['summary']}")

    return results


if __name__ == "__main__":
    main()
