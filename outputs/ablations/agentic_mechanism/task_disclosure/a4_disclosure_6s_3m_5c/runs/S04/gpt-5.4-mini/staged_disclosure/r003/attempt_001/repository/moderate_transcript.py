import os
from typing import Any, Dict, List

from openai import OpenAI


def moderate_transcript(transcript: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=transcript,
    )
    result = response.results[0]
    categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)
    category_scores = result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores)
    flagged_categories: List[str] = [name for name, flagged in categories.items() if flagged]
    return {
        "flagged": bool(result.flagged),
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
    }


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    output = moderate_transcript(text)
    print(output)
