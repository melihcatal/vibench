"""
Moderate transcript text before publishing using the OpenAI Moderation API.

Sends transcript segments to OpenAI's moderation endpoint and returns
flag results with category scores for content safety screening.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def moderate_text(text: str) -> Dict[str, Any]:
    """
    Submit text to OpenAI Moderation API for content safety analysis.

    Parameters
    ----------
    text : str
        The text to moderate.

    Returns
    -------
    dict
        Moderation result containing flagged status and category scores.
    """
    api_key = get_openai_api_key()

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "input": text,
            "model": OPENAI_MODERATION_MODEL,
        },
    )
    response.raise_for_status()
    result = response.json()

    moderation_result = result["results"][0]
    return {
        "flagged": moderation_result["flagged"],
        "categories": moderation_result["categories"],
        "category_scores": moderation_result["category_scores"],
    }


def moderate_transcript_segments(
    segments: List[str],
    threshold: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Moderate a list of transcript segments using OpenAI Moderation API.

    Parameters
    ----------
    segments : list[str]
        List of transcript text segments to moderate.
    threshold : float
        Score threshold above which a category is considered flagged.

    Returns
    -------
    list[dict]
        Each dict contains segment index, text, flagged status, and high-scoring categories.
    """
    results = []
    for i, segment in enumerate(segments):
        if not segment.strip():
            continue

        mod_result = moderate_text(segment)
        high_score_categories = {
            cat: score
            for cat, score in mod_result["category_scores"].items()
            if score >= threshold
        }

        results.append({
            "segment_index": i,
            "text": segment[:200] + ("..." if len(segment) > 200 else ""),
            "flagged": mod_result["flagged"],
            "high_score_categories": high_score_categories,
            "all_scores": mod_result["category_scores"],
        })

    return results


def is_transcript_safe(segments: List[str], threshold: float = 0.5) -> bool:
    """
    Check if all transcript segments pass moderation.
    """
    for segment in segments:
        if not segment.strip():
            continue
        result = moderate_text(segment)
        if result["flagged"]:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Moderate transcript segments with OpenAI")
    parser.add_argument("transcript", help="Transcript text or JSON file path")
    parser.add_argument("--threshold", type=float, default=0.5, help="Flagging threshold")
    parser.add_argument("--input-format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.input_format == "json":
        with open(args.transcript) as f:
            data = json.load(f)
            if isinstance(data, list):
                segments = [seg.get("text", str(seg)) for seg in data]
            else:
                segments = [data.get("text", str(data))]
    else:
        try:
            with open(args.transcript) as f:
                text = f.read()
        except FileNotFoundError:
            text = args.transcript
        segments = [text]

    results = moderate_transcript_segments(segments, threshold=args.threshold)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
