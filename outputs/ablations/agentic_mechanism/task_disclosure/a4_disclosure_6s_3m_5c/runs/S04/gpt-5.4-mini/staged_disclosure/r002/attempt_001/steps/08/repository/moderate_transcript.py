import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def moderate_transcript(transcript: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=transcript)
    item = result.results[0]
    return {
        "flagged": item.flagged,
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
    }


def moderate_transcript_lines(lines: List[str]) -> Dict[str, Any]:
    return moderate_transcript("\n".join(lines))


def main(transcript: Optional[str] = None) -> Dict[str, Any]:
    if transcript is None:
        transcript = os.environ.get("TRANSCRIPT_TEXT", "")
    return moderate_transcript(transcript)
