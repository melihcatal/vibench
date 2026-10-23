"""
Translate completed transcript segments using the DeepL API.

Takes transcript segments and translates them to a target language
using DeepL's translation service.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def get_deepl_api_key() -> str:
    """Retrieve DeepL API key from environment."""
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return api_key


def translate_segments(
    segments: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    preserve_formatting: bool = True,
) -> List[Dict[str, Any]]:
    """
    Translate a list of transcript segments using DeepL API.

    Parameters
    ----------
    segments : list[str]
        List of text segments to translate.
    target_lang : str
        Target language code (e.g., 'EN', 'ES', 'FR', 'DE', 'JA').
    source_lang : str, optional
        Source language code. If None, DeepL auto-detects.
    preserve_formatting : bool
        Preserve formatting tags in the translation.

    Returns
    -------
    list[dict]
        Each dict contains original text, translated text, and detected language.
    """
    api_key = get_deepl_api_key()

    if not segments:
        return []

    payload = {
        "text": segments,
        "target_lang": target_lang.upper(),
    }

    if source_lang:
        payload["source_lang"] = source_lang.upper()

    if preserve_formatting:
        payload["tag_handling"] = "xml"

    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data=payload,
    )
    response.raise_for_status()
    result = response.json()

    translations = []
    for i, translation in enumerate(result.get("translations", [])):
        translations.append({
            "original": segments[i] if i < len(segments) else "",
            "translated": translation.get("text", ""),
            "detected_source_language": translation.get("detected_source_language", source_lang),
        })

    return translations


def translate_transcript(
    transcript_text: str,
    target_lang: str = "EN",
    segment_max_length: int = 5000,
) -> List[Dict[str, Any]]:
    """
    Split transcript text into segments and translate via DeepL.

    DeepL has a character limit per request, so long transcripts
    are split into manageable chunks.
    """
    # Split by utterance boundaries if possible, otherwise by character limit
    raw_segments = []
    current = ""
    for char in transcript_text:
        current += char
        if char in ('.', '!', '?', '\n') and len(current) > 100:
            raw_segments.append(current.strip())
            current = ""
    if current.strip():
        raw_segments.append(current.strip())

    # Ensure no segment exceeds DeepL limits
    final_segments = []
    for seg in raw_segments:
        if len(seg) <= segment_max_length:
            final_segments.append(seg)
        else:
            for i in range(0, len(seg), segment_max_length):
                final_segments.append(seg[i:i + segment_max_length])

    return translate_segments(final_segments, target_lang)


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate transcript segments with DeepL")
    parser.add_argument("transcript", help="Transcript text or JSON file path")
    parser.add_argument("--target-lang", default="EN", help="Target language code")
    parser.add_argument("--source-lang", help="Source language code (optional)")
    parser.add_argument("--input-format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.input_format == "json":
        with open(args.transcript) as f:
            data = json.load(f)
            segments = [seg.get("text", seg) for seg in data] if isinstance(data, list) else [data.get("text", str(data))]
    else:
        try:
            with open(args.transcript) as f:
                text = f.read()
        except FileNotFoundError:
            text = args.transcript
        segments = [text]

    results = translate_segments(segments, args.target_lang, args.source_lang)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
