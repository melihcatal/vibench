"""
moderate_transcript.py - Moderate transcript text before publishing.

Uses OpenAI's moderation API and content filtering to evaluate transcript
segments for potentially harmful, offensive, or inappropriate content.
Returns moderation scores and flags for each segment.

OpenAI Moderation API: https://api.openai.com/v1/moderations
Model: omni-moderation-latest
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import List, Dict, Any, Optional

import requests

from speech_models import ModerationResult

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# OpenAI-specific moderation configuration
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODERATION_ENDPOINT = f"{OPENAI_API_BASE}/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"

# Threshold for flagging content
DEFAULT_FLAG_THRESHOLD = 0.5


class OpenAIConfig:
    """OpenAI API configuration."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        self.timeout = 15

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def moderate_segment(
    text: str,
    config: Optional[OpenAIConfig] = None,
) -> Dict[str, Any]:
    """
    Moderate a single text segment using OpenAI's moderation API.

    Uses omni-moderation-latest model for comprehensive content analysis.

    Args:
        text: The text segment to moderate
        config: OpenAI configuration

    Returns:
        Moderation result with category scores and flags
    """
    config = config or OpenAIConfig()

    payload = {
        "input": text,
        "model": OPENAI_MODERATION_MODEL,  # OpenAI moderation model
    }

    response = requests.post(
        OPENAI_MODERATION_ENDPOINT,
        headers=config.headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    result = response.json()

    # Parse OpenAI moderation response
    moderation = result["results"][0]
    return {
        "flagged": moderation.get("flagged", False),
        "categories": moderation.get("categories", {}),
        "category_scores": moderation.get("category_scores", {}),
    }


def moderate_transcript_segments(
    segments: List[str],
    flag_threshold: float = DEFAULT_FLAG_THRESHOLD,
    config: Optional[OpenAIConfig] = None,
) -> List[ModerationResult]:
    """
    Moderate all segments of a transcript using OpenAI moderation API.

    Args:
        segments: List of transcript segment texts
        flag_threshold: Score threshold for flagging content
        config: OpenAI configuration

    Returns:
        List of ModerationResult objects for each segment
    """
    config = config or OpenAIConfig()
    results = []

    # OpenAI moderation API can handle multiple inputs
    batch_size = 20
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]

        payload = {
            "input": batch,
            "model": OPENAI_MODERATION_MODEL,
        }

        response = requests.post(
            OPENAI_MODERATION_ENDPOINT,
            headers=config.headers,
            json=payload,
            timeout=config.timeout,
        )
        response.raise_for_status()
        result = response.json()

        for j, mod_result in enumerate(result["results"]):
            segment_idx = i + j
            flagged = mod_result.get("flagged", False)
            category_scores = mod_result.get("category_scores", {})

            # Determine highest severity category
            max_score = 0.0
            severity_category = "none"
            for cat, score in category_scores.items():
                if score > max_score:
                    max_score = score
                    severity_category = cat

            severity = "none"
            if max_score > 0.8:
                severity = "high"
            elif max_score > 0.5:
                severity = "medium"
            elif max_score > 0.1:
                severity = "low"

            results.append(ModerationResult(
                segment_index=segment_idx,
                flagged=flagged,
                categories=category_scores,
                severity=severity,
                rationale=f"Highest score: {severity_category} ({max_score:.3f})",
            ))

    logger.info(
        "Moderated %d segments using OpenAI %s. Flagged: %d",
        len(results),
        OPENAI_MODERATION_MODEL,
        sum(1 for r in results if r.flagged),
    )

    return results


def moderate_transcript_from_json(
    transcript_json_path: str,
    flag_threshold: float = DEFAULT_FLAG_THRESHOLD,
) -> List[ModerationResult]:
    """
    Load transcript from JSON and moderate all segments.

    Args:
        transcript_json_path: Path to transcript JSON file
        flag_threshold: Score threshold for flagging

    Returns:
        List of ModerationResult objects
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = []
    for seg in data.get("segments", []):
        if isinstance(seg, dict):
            segments.append(seg.get("text", ""))
        else:
            segments.append(str(seg))

    return moderate_transcript_segments(segments, flag_threshold)


def format_moderation_output(results: List[ModerationResult]) -> str:
    """Format moderation results for display."""
    flagged_count = sum(1 for r in results if r.flagged)
    lines = [
        f"Content Moderation Report (OpenAI {OPENAI_MODERATION_MODEL})",
        f"Segments analyzed: {len(results)}",
        f"Flagged segments: {flagged_count}",
        "=" * 80,
    ]

    for result in results:
        status = "FLAGGED" if result.flagged else "OK"
        lines.append(f"\nSegment {result.segment_index} [{status}] (Severity: {result.severity})")
        lines.append(f"  Rationale: {result.rationale}")
        if result.categories:
            lines.append("  Categories:")
            for cat, score in sorted(result.categories.items(), key=lambda x: -x[1]):
                if score > 0.01:
                    lines.append(f"    {cat}: {score:.3f}")

    return "\n".join(lines)


def get_publishing_recommendation(results: List[ModerationResult]) -> Dict[str, Any]:
    """Generate overall publishing recommendation based on moderation results."""
    flagged = [r for r in results if r.flagged]
    high_severity = [r for r in results if r.severity == "high"]

    if high_severity:
        recommendation = "REJECT"
        reason = f"{len(high_severity)} segments with high severity content detected"
    elif flagged:
        recommendation = "REVIEW"
        reason = f"{len(flagged)} segments flagged for manual review"
    else:
        recommendation = "APPROVE"
        reason = "No concerning content detected"

    return {
        "recommendation": recommendation,
        "reason": reason,
        "total_segments": len(results),
        "flagged_count": len(flagged),
        "high_severity_count": len(high_severity),
    }


def main():
    parser = argparse.ArgumentParser(description="Moderate transcript content using OpenAI moderation API")
    parser.add_argument("transcript_json", help="Path to transcript JSON file")
    parser.add_argument("--threshold", type=float, default=DEFAULT_FLAG_THRESHOLD, help="Flag threshold")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--recommendation", action="store_true", help="Show publishing recommendation")
    args = parser.parse_args()

    results = moderate_transcript_from_json(args.transcript_json, args.threshold)

    if args.json:
        output = [
            {
                "segment_index": r.segment_index,
                "flagged": r.flagged,
                "categories": r.categories,
                "severity": r.severity,
                "rationale": r.rationale,
            }
            for r in results
        ]
        print(json.dumps(output, indent=2))
    elif args.recommendation:
        rec = get_publishing_recommendation(results)
        print(json.dumps(rec, indent=2))
    else:
        print(format_moderation_output(results))


if __name__ == "__main__":
    main()
