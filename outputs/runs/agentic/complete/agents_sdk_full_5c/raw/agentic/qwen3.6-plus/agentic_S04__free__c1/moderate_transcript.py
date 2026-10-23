"""
Moderate transcript text before publishing.
Provider: OpenAI Moderation API (api.openai.com)
SDK: openai Python client for content moderation checks.
"""

import logging
import os
from typing import List, Dict, Any, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_HOST = "api.openai.com"
MODERATION_MODEL = "omni-moderation-latest"


def create_openai_client() -> OpenAI:
    """
    Create an OpenAI client for moderation API calls.
    
    Provider: OpenAI (api.openai.com)
    SDK: openai Python package
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    client = OpenAI(api_key=api_key)
    logger.info(f"Initialized OpenAI client for {OPENAI_API_HOST}")
    return client


def moderate_text(text: str) -> Dict[str, Any]:
    """
    Moderate a single text segment using OpenAI Moderation API.
    
    Provider: OpenAI api.openai.com
    Model: omni-moderation-latest for content safety classification.
    
    Args:
        text: Text segment to moderate
        
    Returns:
        Dict with moderation results including flagged status and categories
    """
    client = create_openai_client()
    
    response = client.moderations.create(
        input=text,
        model=MODERATION_MODEL,
    )
    
    result = response.results[0]
    
    return {
        "text": text,
        "flagged": result.flagged,
        "categories": {
            "sexual": result.categories.sexual,
            "hate": result.categories.hate,
            "harassment": result.categories.harassment,
            "self-harm": result.categories.self_harm,
            "sexual/minors": result.categories.sexual_minors,
            "hate/threatening": result.categories.hate_threatening,
            "violence/graphic": result.categories.violence_graphic,
            "self-harm/intent": result.categories.self_harm_intent,
            "self-harm/instructions": result.categories.self_harm_instructions,
            "harassment/threatening": result.categories.harassment_threatening,
            "violence": result.categories.violence,
        },
        "category_scores": {
            "sexual": result.category_scores.sexual,
            "hate": result.category_scores.hate,
            "harassment": result.category_scores.harassment,
            "self-harm": result.category_scores.self_harm,
            "sexual/minors": result.category_scores.sexual_minors,
            "hate/threatening": result.category_scores.hate_threatening,
            "violence/graphic": result.category_scores.violence_graphic,
            "self-harm/intent": result.category_scores.self_harm_intent,
            "self-harm/instructions": result.category_scores.self_harm_instructions,
            "harassment/threatening": result.category_scores.harassment_threatening,
            "violence": result.category_scores.violence,
        },
        "provider": "openai",
        "api_host": OPENAI_API_HOST,
        "model": MODERATION_MODEL,
    }


def moderate_transcript_segments(
    segments: List[str],
    flag_threshold: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Moderate multiple transcript segments using OpenAI Moderation API.
    
    Provider: OpenAI api.openai.com with omni-moderation-latest model.
    Checks each segment for harmful content categories.
    
    Args:
        segments: List of text segments to moderate
        flag_threshold: Confidence threshold for flagging (default 0.5)
        
    Returns:
        List of moderation results for each segment
    """
    results = []
    for segment in segments:
        if not segment.strip():
            continue
        
        moderation = moderate_text(segment)
        
        # Check if any category exceeds threshold
        high_confidence_flags = [
            cat for cat, score in moderation["category_scores"].items()
            if score >= flag_threshold
        ]
        
        moderation["high_confidence_flags"] = high_confidence_flags
        moderation["is_safe"] = len(high_confidence_flags) == 0
        
        results.append(moderation)
    
    return results


def moderate_full_transcript(
    transcript_text: str,
    segment_size: int = 500,
) -> Dict[str, Any]:
    """
    Moderate a full transcript by splitting into segments.
    
    Uses OpenAI's omni-moderation-latest model at api.openai.com.
    Splits long transcripts for comprehensive moderation coverage.
    
    Args:
        transcript_text: Full transcript text
        segment_size: Characters per segment for moderation
        
    Returns:
        Dict with overall moderation status and per-segment results
    """
    # Split transcript into segments
    segments = []
    for i in range(0, len(transcript_text), segment_size):
        segment = transcript_text[i:i + segment_size]
        # Try to break at sentence boundary
        last_period = segment.rfind(". ")
        if last_period > segment_size // 2:
            segment = segment[:last_period + 1]
        segments.append(segment.strip())
    
    results = moderate_transcript_segments(segments)
    
    # Aggregate results
    flagged_segments = [r for r in results if r.get("flagged")]
    
    return {
        "total_segments": len(results),
        "flagged_segments": len(flagged_segments),
        "is_safe": len(flagged_segments) == 0,
        "flagged_details": flagged_segments,
        "provider": "openai",
        "model": MODERATION_MODEL,
    }


def filter_safe_segments(
    segments: List[str],
) -> List[str]:
    """
    Filter transcript segments, keeping only those that pass moderation.
    
    Uses OpenAI moderation api.openai.com to remove flagged content.
    """
    results = moderate_transcript_segments(segments)
    return [r["text"] for r in results if r.get("is_safe", True)]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = moderate_text(text)
        print(f"Flagged: {result['flagged']}")
        print(f"Categories: {result['categories']}")
    else:
        print("Usage: python moderate_transcript.py <text>")
