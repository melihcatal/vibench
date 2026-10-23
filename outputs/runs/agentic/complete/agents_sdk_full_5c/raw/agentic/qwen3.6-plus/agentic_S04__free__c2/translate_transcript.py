"""
translate_transcript.py - Translate completed transcript segments.

Uses OpenAI's GPT models to translate transcript segments into a target language.
Processes segments from a completed transcription and returns translated text.

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
        self.timeout = 30

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def translate_segments(
    segments: List[str],
    target_language: str,
    source_language: str = "en",
    config: Optional[OpenAIConfig] = None,
    preserve_speaker_labels: bool = True,
) -> List[Dict[str, str]]:
    """
    Translate transcript segments using OpenAI's gpt-4o model.

    Args:
        segments: List of transcript segment texts to translate
        target_language: Target language code (e.g., "es", "fr", "ja")
        source_language: Source language code (default: "en")
        config: OpenAI configuration (optional)
        preserve_speaker_labels: Whether to preserve speaker label formatting

    Returns:
        List of dicts with original and translated text
    """
    config = config or OpenAIConfig()

    # Batch segments for efficient API calls (up to 10 segments per request)
    batch_size = 10
    translated_results = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        
        # Build translation prompt for OpenAI gpt-4o
        system_prompt = (
            f"You are a professional translator. Translate the following transcript segments "
            f"from {source_language} to {target_language}. "
            f"Preserve any speaker labels, timestamps, or formatting. "
            f"Maintain the original tone and context. "
            f"Return the translations as a JSON array of strings."
        )

        if preserve_speaker_labels:
            system_prompt += (
                " If segments contain speaker identifiers like '[Speaker A]', keep them intact."
            )

        user_content = "\n".join(
            f"{j + 1}. {seg}" for j, seg in enumerate(batch)
        )

        payload = {
            "model": OPENAI_MODEL,  # OpenAI gpt-4o model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.3,
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

        # Parse translated segments from OpenAI response
        content = result["choices"][0]["message"]["content"]
        try:
            translations = json.loads(content)
            # Handle various response formats
            if isinstance(translations, dict):
                translations = list(translations.values())
            elif isinstance(translations, list):
                pass
            else:
                translations = [translations]
        except json.JSONDecodeError:
            # Fallback: treat content as single translation
            translations = [content]

        for j, original in enumerate(batch):
            translated = translations[j] if j < len(translations) else original
            translated_results.append({
                "original": original,
                "translated": translated,
                "source_language": source_language,
                "target_language": target_language,
            })

    logger.info(
        "Translated %d segments to %s using OpenAI %s",
        len(translated_results),
        target_language,
        OPENAI_MODEL,
    )

    return translated_results


def translate_transcript_from_json(
    transcript_json_path: str,
    target_language: str,
    source_language: str = "en",
) -> List[Dict[str, str]]:
    """
    Load transcript from JSON and translate all segments.

    Args:
        transcript_json_path: Path to transcript JSON file with 'segments' key
        target_language: Target language code
        source_language: Source language code

    Returns:
        List of translation results
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = []
    for seg in data.get("segments", []):
        if isinstance(seg, dict):
            segments.append(seg.get("text", ""))
        else:
            segments.append(str(seg))

    return translate_segments(segments, target_language, source_language)


def format_translation_output(results: List[Dict[str, str]]) -> str:
    """Format translation results for display."""
    lines = [
        f"Translation Results (via OpenAI {OPENAI_MODEL})",
        f"Segments: {len(results)}",
        "=" * 80,
    ]

    for i, result in enumerate(results, 1):
        lines.append(f"\n--- Segment {i} ---")
        lines.append(f"  Original: {result['original']}")
        lines.append(f"  Translated ({result['target_language']}): {result['translated']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Translate transcript segments using OpenAI gpt-4o")
    parser.add_argument("transcript_json", help="Path to transcript JSON file")
    parser.add_argument("--target", required=True, help="Target language code (e.g., es, fr, ja)")
    parser.add_argument("--source", default="en", help="Source language code (default: en)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    results = translate_transcript_from_json(
        args.transcript_json,
        target_language=args.target,
        source_language=args.source,
    )

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_translation_output(results))


if __name__ == "__main__":
    main()
