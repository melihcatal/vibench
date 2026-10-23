"""
archive_summary.py - Summarize transcription results.

Uses OpenAI's GPT models to generate summaries, key points, and topic extraction
from completed transcription results for archival and review purposes.

OpenAI API: https://api.openai.com/v1/chat/completions
Model: gpt-4o
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import List, Dict, Any, Optional

import requests

from speech_models import TranscriptSummary

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# OpenAI-specific configuration
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_CHAT_ENDPOINT = f"{OPENAI_API_BASE}/chat/completions"
OPENAI_MODEL = "gpt-4o"


class OpenAIConfig:
    """OpenAI API configuration."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        self.model = OPENAI_MODEL
        self.timeout = 60

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def generate_summary(
    transcript_text: str,
    config: Optional[OpenAIConfig] = None,
    summary_type: str = "comprehensive",
    max_length: int = 500,
) -> TranscriptSummary:
    """
    Generate a summary of transcript text using OpenAI gpt-4o.

    Args:
        transcript_text: Full transcript text to summarize
        config: OpenAI configuration
        summary_type: Type of summary (comprehensive, executive, bullet)
        max_length: Maximum summary length in words

    Returns:
        TranscriptSummary with summary text, key points, topics, and sentiment
    """
    config = config or OpenAIConfig()

    system_prompts = {
        "comprehensive": (
            "You are an expert meeting summarizer. Create a comprehensive summary "
            "of the following transcript including key decisions, action items, "
            "and important discussion points."
        ),
        "executive": (
            "You are an executive assistant. Create a concise executive summary "
            "of the following transcript highlighting only the most critical "
            "information and outcomes."
        ),
        "bullet": (
            "You are a professional note-taker. Create a bulleted summary of "
            "the following transcript with clear, concise points."
        ),
    }

    system_prompt = system_prompts.get(summary_type, system_prompts["comprehensive"])
    system_prompt += f" Keep the summary under {max_length} words."

    # Request structured JSON output from OpenAI gpt-4o
    user_content = (
        f"Analyze this transcript and return a JSON object with:\n"
        f"- summary_text: A paragraph summary\n"
        f"- key_points: Array of 3-7 key points\n"
        f"- topics: Array of main topics discussed\n"
        f"- sentiment: Overall sentiment (positive, negative, neutral, mixed)\n\n"
        f"Transcript:\n{transcript_text}"
    )

    payload = {
        "model": OPENAI_MODEL,  # OpenAI gpt-4o model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.5,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_CHAT_ENDPOINT,
        headers=config.headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    result = response.json()

    # Parse OpenAI response
    content = result["choices"][0]["message"]["content"]
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {
            "summary_text": content,
            "key_points": [],
            "topics": [],
            "sentiment": "neutral",
        }

    summary = TranscriptSummary(
        summary_text=data.get("summary_text", ""),
        key_points=data.get("key_points", []),
        topics=data.get("topics", []),
        sentiment=data.get("sentiment", "neutral"),
    )

    logger.info(
        "Generated %s summary using OpenAI %s (%d key points, %d topics)",
        summary_type,
        OPENAI_MODEL,
        len(summary.key_points),
        len(summary.topics),
    )

    return summary


def summarize_from_json(
    transcript_json_path: str,
    summary_type: str = "comprehensive",
) -> TranscriptSummary:
    """
    Load transcript from JSON and generate summary.

    Args:
        transcript_json_path: Path to transcript JSON file
        summary_type: Type of summary to generate

    Returns:
        TranscriptSummary object
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract full text from transcript
    transcript_text = data.get("text", "")
    if not transcript_text:
        segments = data.get("segments", [])
        transcript_text = " ".join(
            seg.get("text", "") if isinstance(seg, dict) else str(seg)
            for seg in segments
        )

    return generate_summary(transcript_text, summary_type=summary_type)


def format_summary_output(summary: TranscriptSummary) -> str:
    """Format summary for display."""
    lines = [
        f"Transcript Summary (via OpenAI {OPENAI_MODEL})",
        f"Sentiment: {summary.sentiment}",
        "=" * 80,
        "",
        "SUMMARY:",
        summary.summary_text,
        "",
        "KEY POINTS:",
    ]

    for i, point in enumerate(summary.key_points, 1):
        lines.append(f"  {i}. {point}")

    lines.append("")
    lines.append("TOPICS:")
    for topic in summary.topics:
        lines.append(f"  - {topic}")

    return "\n".join(lines)


def generate_archive_record(
    transcript_json_path: str,
    summary_type: str = "comprehensive",
) -> Dict[str, Any]:
    """
    Generate a complete archive record with summary and metadata.
    Uses OpenAI gpt-4o for summarization.

    Args:
        transcript_json_path: Path to transcript JSON
        summary_type: Summary type

    Returns:
        Archive record dict with summary and metadata
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = generate_summary(
        data.get("text", ""),
        summary_type=summary_type,
    )

    return {
        "transcription_id": data.get("transcription_id", ""),
        "audio_duration": data.get("audio_duration", 0),
        "summary": summary.summary_text,
        "key_points": summary.key_points,
        "topics": summary.topics,
        "sentiment": summary.sentiment,
        "model_used": OPENAI_MODEL,
    }


def main():
    parser = argparse.ArgumentParser(description="Summarize transcription results using OpenAI gpt-4o")
    parser.add_argument("transcript_json", help="Path to transcript JSON file")
    parser.add_argument("--type", default="comprehensive", choices=["comprehensive", "executive", "bullet"])
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--archive", action="store_true", help="Generate full archive record")
    args = parser.parse_args()

    if args.archive:
        record = generate_archive_record(args.transcript_json, args.type)
        print(json.dumps(record, indent=2, ensure_ascii=False))
    else:
        summary = summarize_from_json(args.transcript_json, args.type)
        if args.json:
            print(json.dumps(
                {
                    "summary_text": summary.summary_text,
                    "key_points": summary.key_points,
                    "topics": summary.topics,
                    "sentiment": summary.sentiment,
                },
                indent=2,
                ensure_ascii=False,
            ))
        else:
            print(format_summary_output(summary))


if __name__ == "__main__":
    main()
