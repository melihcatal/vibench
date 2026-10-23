import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_live_transcript_safety(transcript_text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(
        model=OPENAI_MODEL,
        input=transcript_text,
    )
    result = response.results[0]
    categories = getattr(result, "categories", None)
    category_scores = getattr(result, "category_scores", None)

    unsafe_categories: List[str] = []
    if categories is not None:
        if hasattr(categories, "model_dump"):
            category_map = categories.model_dump()
        elif hasattr(categories, "dict"):
            category_map = categories.dict()
        else:
            category_map = dict(categories)
        unsafe_categories = [name for name, flagged in category_map.items() if flagged]

    scores: Dict[str, float] = {}
    if category_scores is not None:
        if hasattr(category_scores, "model_dump"):
            scores = category_scores.model_dump()
        elif hasattr(category_scores, "dict"):
            scores = category_scores.dict()
        else:
            scores = dict(category_scores)

    return {
        "unsafe": bool(result.flagged),
        "unsafe_categories": unsafe_categories,
        "category_scores": scores,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }


def main() -> None:
    transcript_text = os.environ.get("LIVE_TRANSCRIPT_TEXT", "")
    output = check_live_transcript_safety(transcript_text)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
