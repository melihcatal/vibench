"""Translate completed transcript segments using Google Cloud Translation API.

Uses the google-cloud-translate SDK for batch translation of transcription text.
Auth: GOOGLE_APPLICATION_CREDENTIALS environment variable.
"""

import os
from typing import List, Optional

from google.cloud import translate_v2 as translate


def translate_segments(
    segments: List[str],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> List[dict]:
    """Translate a list of transcript segments using Google Cloud Translation API.

    Args:
        segments: List of text segments to translate.
        target_language: ISO 639-1 target language code (e.g., 'es', 'fr', 'ja').
        source_language: Optional source language code. Auto-detected if None.

    Returns:
        List of dicts with keys 'index', 'original', 'translated'.
    """
    client = translate.Client()

    translate_kwargs: dict = {"target_language": target_language}
    if source_language:
        translate_kwargs["source_language"] = source_language

    # Google Translate API accepts a list for batch translation
    results = client.translate(segments, **translate_kwargs)

    # Normalize: client.translate returns a single dict or a list of dicts
    if isinstance(results, dict):
        results = [results]

    output = []
    for i, (segment, translation) in enumerate(zip(segments, results)):
        output.append({
            "index": i,
            "original": segment,
            "translated": translation.get("translatedText", ""),
            "detected_source": translation.get("detectedSourceLanguage", ""),
            "target_language": target_language,
        })

    return output


def translate_full_transcript(
    transcript: str,
    target_language: str = "es",
    segment_size: int = 500,
) -> List[dict]:
    """Translate a full transcript by splitting into chunks.

    Splits the transcript into segments of up to segment_size characters
    and translates each batch via Google Cloud Translation.
    """
    # Simple chunking by character count
    chunks = [
        transcript[i : i + segment_size]
        for i in range(0, len(transcript), segment_size)
    ]
    return translate_segments(chunks, target_language=target_language)


def main():
    import json
    import sys

    target_lang = sys.argv[2] if len(sys.argv) > 2 else "es"

    # Read segments from stdin as JSON array if provided
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
        segments = data if isinstance(data, list) else data.get("segments", [data.get("text", "")])
    else:
        segments = ["Hello, how are you today?", "The meeting starts at 3pm."]

    results = translate_segments(segments, target_language=target_lang)
    for r in results:
        print(f"[{r['index']}] {r['original']} -> {r['translated']}")


if __name__ == "__main__":
    main()
