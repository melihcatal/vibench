"""
Summarize transcription results using the OpenAI Chat Completions API.

Generates concise summaries of transcript text for archival and
quick reference purposes.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def generate_summary(
    transcript_text: str,
    max_length: int = 500,
    summary_type: str = "executive",
) -> Dict[str, Any]:
    """
    Generate a summary of transcript text using OpenAI GPT-4o-mini.

    Parameters
    ----------
    transcript_text : str
        Full transcript text to summarize.
    max_length : int
        Maximum summary length in characters.
    summary_type : str
        Type of summary: 'executive', 'detailed', or 'bullet'.

    Returns
    -------
    dict
        Contains the generated summary and metadata.
    """
    api_key = get_openai_api_key()

    prompt_templates = {
        "executive": (
            f"Provide an executive summary of the following transcript. "
            f"Keep it concise, under {max_length} characters. Focus on key decisions, "
            f"action items, and outcomes.\n\nTranscript:\n{transcript_text}"
        ),
        "detailed": (
            f"Provide a detailed summary of the following transcript. "
            f"Include all major topics discussed, key points, and conclusions. "
            f"Keep it under {max_length} characters.\n\nTranscript:\n{transcript_text}"
        ),
        "bullet": (
            f"Convert the following transcript into a bulleted summary. "
            f"Each bullet should capture a distinct topic or decision. "
            f"Keep the total under {max_length} characters.\n\nTranscript:\n{transcript_text}"
        ),
    }

    system_prompt = (
        "You are a professional meeting note summarizer. "
        "Create clear, accurate summaries that capture the essential content."
    )

    response = requests.post(
        OPENAI_CHAT_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_SUMMARY_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_templates.get(summary_type, prompt_templates["executive"])},
            ],
            "max_tokens": 1000,
            "temperature": 0.3,
        },
    )
    response.raise_for_status()
    result = response.json()

    summary_text = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})

    return {
        "summary": summary_text,
        "summary_type": summary_type,
        "original_length": len(transcript_text),
        "summary_length": len(summary_text),
        "compression_ratio": round(len(summary_text) / max(len(transcript_text), 1), 4),
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
    }


def summarize_segments(
    segments: List[str],
    summary_type: str = "executive",
) -> List[Dict[str, Any]]:
    """
    Generate summaries for individual transcript segments.
    """
    results = []
    for i, segment in enumerate(segments):
        if not segment.strip():
            continue
        summary = generate_summary(segment, max_length=300, summary_type=summary_type)
        summary["segment_index"] = i
        results.append(summary)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize transcript with OpenAI")
    parser.add_argument("transcript", help="Transcript text or JSON file path")
    parser.add_argument("--type", choices=["executive", "detailed", "bullet"], default="executive")
    parser.add_argument("--max-length", type=int, default=500, help="Max summary length")
    parser.add_argument("--input-format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.input_format == "json":
        with open(args.transcript) as f:
            data = json.load(f)
            if isinstance(data, list):
                segments = [seg.get("text", str(seg)) for seg in data]
                results = summarize_segments(segments, summary_type=args.type)
            else:
                text = data.get("text", str(data))
                results = generate_summary(text, max_length=args.max_length, summary_type=args.type)
    else:
        try:
            with open(args.transcript) as f:
                text = f.read()
        except FileNotFoundError:
            text = args.transcript
        results = generate_summary(text, max_length=args.max_length, summary_type=args.type)

    if isinstance(results, list):
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
