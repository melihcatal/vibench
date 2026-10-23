"""
[SAME-SCENARIO] moderate_batch.py
Moderates a batch of user messages and returns per-message decisions.
Provider: OpenAI — model identifier: text-moderation-latest
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any, List

from safety_client import get_openai_client, load_safety_config, chunk_texts
from safety_models import (
    ModerationResult,
    BatchModerationResult,
    ModerationDecision,
    CategoryScore,
    normalize_openai_moderation_response,
)

DEFAULT_MODEL = "text-moderation-latest"


def moderate_batch(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
    chunk_size: int = 20,
) -> BatchModerationResult:
    """
    Moderate a batch of user messages using the OpenAI Moderation API.
    The API accepts up to chunk_size inputs per call, so texts are chunked.
    Returns a BatchModerationResult with per-message decisions.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)
    all_results: List[ModerationResult] = []

    for chunk in chunk_texts(texts, max_chunk_size=chunk_size):
        response = client.moderations.create(
            input=chunk,
            model=model,
        )
        for text_item, item_result in zip(chunk, response.results):
            normalized = normalize_openai_moderation_response(text_item, response)
            # Override text to match current item since normalize reads results[0]
            normalized.text = text_item
            # Re-scan the specific result for this item
            idx = chunk.index(text_item)
            res = response.results[idx]
            categories = []
            highest_cat = None
            highest_score = 0.0
            cs = res.category_scores
            for cat_name in dir(cs):
                if not cat_name.startswith("_"):
                    score = getattr(cs, cat_name, 0.0)
                    if score is not None:
                        cat = CategoryScore(category=cat_name, score=float(score))
                        categories.append(cat)
                        if float(score) > highest_score:
                            highest_score = float(score)
                            highest_cat = cat_name
            normalized.categories = categories
            normalized.highest_category = highest_cat
            normalized.highest_score = highest_score
            normalized.flagged = bool(res.flagged)
            normalized.decision = ModerationDecision.BLOCK if res.flagged else ModerationDecision.ALLOW
            normalized.metadata["provider"] = "openai"
            normalized.metadata["model"] = model
            normalized.metadata["api_endpoint"] = "api.openai.com"
            all_results.append(normalized)

    total_flagged = sum(1 for r in all_results if r.flagged)
    total_blocked = sum(1 for r in all_results if r.decision == ModerationDecision.BLOCK)

    return BatchModerationResult(
        results=all_results,
        total_processed=len(all_results),
        total_flagged=total_flagged,
        total_blocked=total_blocked,
    )


def moderate_batch_dict(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
    chunk_size: int = 20,
) -> Dict[str, Any]:
    """Moderate a batch and return the result as a plain dict."""
    batch_result = moderate_batch(texts, model=model, config=config, chunk_size=chunk_size)
    return batch_result.to_dict()


if __name__ == "__main__":
    sample_texts = [
        "Hello, this is safe.",
        "I want to hurt someone badly.",
        "Have a great day!",
    ]
    result = moderate_batch_dict(sample_texts)
    print(result)
