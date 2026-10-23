import os
import requests
import json
from typing import List, Dict, Any
from speech_models import TranscriptionResult


def moderate_transcript_text(
    transcript: TranscriptionResult, categories: List[str] = None
) -> Dict[str, Any]:
    """
    Moderate transcript text before publishing using Perspective API.

    Args:
        transcript: TranscriptionResult object
        categories: List of toxicity categories to check

    Returns:
        Dictionary with moderation results
    """
    # Get Perspective API key from environment
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    # Default categories to check
    if categories is None:
        categories = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    # Prepare text for moderation
    text_to_moderate = transcript.transcript

    # Split into chunks if text is too long (Perspective API has limits)
    max_chunk_size = 20000  # characters
    chunks = []
    if len(text_to_moderate) > max_chunk_size:
        # Split by sentences
        import re

        sentences = re.split(r"(?<=[.!?])\s+", text_to_moderate)
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)
    else:
        chunks = [text_to_moderate]

    # Call Perspective API for each chunk
    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    all_results = []
    for i, chunk in enumerate(chunks):
        request_data = {
            "comment": {"text": chunk, "type": "PLAIN_TEXT"},
            "languages": ["en"],
            "requestedAttributes": {category: {} for category in categories},
            "doNotStore": True,
        }

        params = {"key": api_key}

        try:
            response = requests.post(
                api_url, params=params, json=request_data, timeout=30
            )
            response.raise_for_status()

            result = response.json()

            # Extract scores
            chunk_result = {"chunk_index": i, "text_length": len(chunk), "scores": {}}

            for category in categories:
                if category in result.get("attributeScores", {}):
                    score = result["attributeScores"][category]["summaryScore"]["value"]
                    chunk_result["scores"][category] = score

            all_results.append(chunk_result)

        except requests.exceptions.RequestException as e:
            print(f"Error calling Perspective API for chunk {i}: {e}")
            all_results.append(
                {
                    "chunk_index": i,
                    "text_length": len(chunk),
                    "error": str(e),
                    "scores": {},
                }
            )

    # Calculate overall scores
    overall_scores = {}
    for category in categories:
        category_scores = [
            r["scores"].get(category, 0) for r in all_results if "scores" in r
        ]
        if category_scores:
            overall_scores[category] = {
                "mean": sum(category_scores) / len(category_scores),
                "max": max(category_scores),
                "min": min(category_scores),
            }

    # Identify problematic segments
    problematic_segments = []
    if hasattr(transcript, "segments") and transcript.segments:
        # Check each segment individually if we have timestamped segments
        for segment in transcript.segments:
            segment_text = segment["text"]
            if len(segment_text) > 10:  # Only check meaningful segments
                segment_result = analyze_text_segment(segment_text, api_key, categories)
                if segment_result.get("has_issues", False):
                    problematic_segments.append(
                        {
                            "text": segment_text,
                            "start_time": segment["start_time"],
                            "end_time": segment["end_time"],
                            "scores": segment_result["scores"],
                        }
                    )

    return {
        "job_id": transcript.job_id,
        "total_chunks": len(chunks),
        "total_text_length": len(text_to_moderate),
        "chunk_results": all_results,
        "overall_scores": overall_scores,
        "problematic_segments": problematic_segments,
        "has_issues": any(
            score["mean"] > 0.7 or score["max"] > 0.9
            for score in overall_scores.values()
        ),
    }


def analyze_text_segment(
    text: str, api_key: str, categories: List[str]
) -> Dict[str, Any]:
    """Analyze a single text segment using Perspective API."""
    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    request_data = {
        "comment": {"text": text, "type": "PLAIN_TEXT"},
        "languages": ["en"],
        "requestedAttributes": {category: {} for category in categories},
        "doNotStore": True,
    }

    params = {"key": api_key}

    try:
        response = requests.post(api_url, params=params, json=request_data, timeout=10)
        response.raise_for_status()

        result = response.json()
        scores = {}

        for category in categories:
            if category in result.get("attributeScores", {}):
                score = result["attributeScores"][category]["summaryScore"]["value"]
                scores[category] = score

        # Determine if segment has issues
        has_issues = any(score > 0.7 for score in scores.values()) or any(
            category in ["TOXICITY", "SEVERE_TOXICITY"]
            and scores.get(category, 0) > 0.5
            for category in scores
        )

        return {"scores": scores, "has_issues": has_issues}

    except requests.exceptions.RequestException as e:
        print(f"Error analyzing text segment: {e}")
        return {"scores": {}, "has_issues": False, "error": str(e)}


def get_moderation_recommendation(moderation_result: Dict[str, Any]) -> str:
    """Get recommendation based on moderation results."""
    if not moderation_result.get("has_issues", False):
        return "Text is safe for publication."

    issues = []
    overall_scores = moderation_result.get("overall_scores", {})

    for category, scores in overall_scores.items():
        if scores["mean"] > 0.7:
            issues.append(f"High {category.lower()} (score: {scores['mean']:.2f})")
        elif scores["max"] > 0.9:
            issues.append(f"Severe {category.lower()} in some segments")

    if issues:
        return f"Consider reviewing before publication. Issues detected: {', '.join(issues)}"

    return "Text may need minor review."


if __name__ == "__main__":
    # Example usage
    import sys

    # Check for Perspective API key
    if not os.environ.get("PERSPECTIVE_API_KEY"):
        print("Please set PERSPECTIVE_API_KEY environment variable")
        sys.exit(1)

    if len(sys.argv) > 1:
        # Create a mock transcript for testing
        mock_transcript = TranscriptionResult(
            job_id="test-job-123", transcript=sys.argv[1], language_code="en-US"
        )

        result = moderate_transcript_text(mock_transcript)
        print(f"Moderation results:")
        print(f"Has issues: {result['has_issues']}")
        print(f"Overall scores: {json.dumps(result['overall_scores'], indent=2)}")
        print(f"Recommendation: {get_moderation_recommendation(result)}")
    else:
        print("Usage: python moderate_transcript.py <text_to_moderate>")
        print("Example: python moderate_transcript.py 'This is a test transcript.'")
