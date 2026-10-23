import os
from typing import Any, Dict, Optional

from openai import OpenAI


def moderate_text(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation_model = model or os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    response = client.moderations.create(model=moderation_model, input=text)
    result = response.results[0]
    categories = dict(result.categories.model_dump()) if hasattr(result.categories, "model_dump") else dict(result.categories)
    category_scores = (
        dict(result.category_scores.model_dump())
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores)
    )
    return {
        "model": moderation_model,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
    }


def main() -> None:
    import json
    import sys

    text = sys.stdin.read()
    output = moderate_text(text)
    sys.stdout.write(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
