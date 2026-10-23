from __future__ import annotations

from typing import Dict, List, Tuple

from model_client import create_moderation
from model_models import ModerationRequest, ModerationResponse


def check_prompt_safety(
    text: str, model: str = "omni-moderation-latest"
) -> ModerationResponse:
    request = ModerationRequest(input_text=text, model=model)
    return create_moderation(request)


def is_content_safe(text: str, model: str = "omni-moderation-latest") -> bool:
    result = check_prompt_safety(text, model=model)
    return not result.flagged


def get_safety_categories(
    text: str, model: str = "omni-moderation-latest"
) -> Dict[str, bool]:
    result = check_prompt_safety(text, model=model)
    return result.categories


def get_safety_scores(
    text: str, model: str = "omni-moderation-latest"
) -> Dict[str, float]:
    result = check_prompt_safety(text, model=model)
    return result.category_scores


def filter_safe_texts(
    texts: List[str], model: str = "omni-moderation-latest"
) -> List[str]:
    return [t for t in texts if is_content_safe(t, model=model)]


def check_batch_safety(
    texts: List[str], model: str = "omni-moderation-latest"
) -> List[Tuple[str, ModerationResponse]]:
    results: List[Tuple[str, ModerationResponse]] = []
    for text in texts:
        response = check_prompt_safety(text, model=model)
        results.append((text, response))
    return results


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = check_prompt_safety(input_text)
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.categories}")
    print(f"Scores: {result.category_scores}")
