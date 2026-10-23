import os
import requests
from typing import List, Dict, Any, Optional

from speech_models import ModerationResult

OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def moderate_text(text: str) -> ModerationResult:
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
    data = response.json()

    result = data["results"][0]
    categories = result["categories"]
    category_scores = result["category_scores"]

    return ModerationResult(
        flagged=result["flagged"],
        categories=categories,
        scores=category_scores,
    )


def moderate_transcript_segments(
    transcript_data: Dict[str, Any],
    threshold: float = 0.5,
) -> Dict[str, Any]:
    text = transcript_data.get("text", "")
    segments = transcript_data.get("segments", [])

    overall_moderation = moderate_text(text)

    flagged_segments = []
    for seg in segments:
        seg_text = seg.get("text", "")
        if seg_text:
            seg_mod = moderate_text(seg_text)
            if seg_mod.flagged:
                flagged_segments.append(
                    {
                        "text": seg_text,
                        "start": seg.get("start", 0),
                        "end": seg.get("end", 0),
                        "speaker": seg.get("speaker"),
                        "flagged_categories": {
                            k: v for k, v in seg_mod.categories.items() if v
                        },
                        "scores": {
                            k: v for k, v in seg_mod.scores.items() if v > threshold
                        },
                    }
                )

    return {
        "provider": "OpenAI",
        "model": OPENAI_MODERATION_MODEL,
        "overall_flagged": overall_moderation.flagged,
        "overall_categories": overall_moderation.categories,
        "overall_scores": overall_moderation.scores,
        "flagged_segment_count": len(flagged_segments),
        "flagged_segments": flagged_segments,
        "safe_to_publish": not overall_moderation.flagged
        and len(flagged_segments) == 0,
    }


def is_safe_to_publish(transcript_data: Dict[str, Any]) -> bool:
    result = moderate_transcript_segments(transcript_data)
    return result["safe_to_publish"]


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else ""
    if not text:
        print("Usage: python moderate_transcript.py <text>")
        sys.exit(1)

    result = moderate_transcript_segments({"text": text})
    print(result)
