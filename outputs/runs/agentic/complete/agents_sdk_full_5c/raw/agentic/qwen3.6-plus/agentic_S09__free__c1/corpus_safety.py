"""Check corpus text before embedding using OpenAI Moderation API."""

import os
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from openai import OpenAI

from embeddings_client import get_openai_client


@dataclass
class SafetyCheckResult:
    """Result of a safety check on a single text."""
    text: str
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    safe_for_embedding: bool = True


@dataclass
class CorpusSafetyReport:
    """Safety report for an entire corpus."""
    total_texts: int
    flagged_count: int
    safe_count: int
    flag_rate: float
    results: List[SafetyCheckResult] = field(default_factory=list)
    flagged_indices: List[int] = field(default_factory=list)
    summary_categories: Dict[str, int] = field(default_factory=dict)


def check_text_safety(
    text: str,
    model: str = "omni-moderation-latest",
) -> SafetyCheckResult:
    """Check if a single text is safe for embedding using OpenAI Moderation API.

    Uses OpenAI's omni-moderation-latest model to detect harmful content.
    https://platform.openai.com/docs/guides/moderation

    Args:
        text: Text to check for safety.
        model: OpenAI moderation model identifier.

    Returns:
        SafetyCheckResult with flagging details.
    """
    client = get_openai_client()

    response = client.moderations.create(
        input=text,
        model=model,
    )

    result_data = response.results[0]
    categories = {}
    category_scores = {}

    if hasattr(result_data, 'categories'):
        cats = result_data.categories
        if hasattr(cats, 'model_dump'):
            cats_dict = cats.model_dump()
        elif hasattr(cats, '__dict__'):
            cats_dict = vars(cats)
        else:
            cats_dict = {}
        categories = {k: v for k, v in cats_dict.items() if isinstance(v, bool)}

    if hasattr(result_data, 'category_scores'):
        scores = result_data.category_scores
        if hasattr(scores, 'model_dump'):
            scores_dict = scores.model_dump()
        elif hasattr(scores, '__dict__'):
            scores_dict = vars(scores)
        else:
            scores_dict = {}
        category_scores = {k: v for k, v in scores_dict.items() if isinstance(v, (int, float))}

    return SafetyCheckResult(
        text=text,
        flagged=result_data.flagged,
        categories=categories,
        category_scores=category_scores,
        safe_for_embedding=not result_data.flagged,
    )


def check_corpus_safety(
    texts: List[str],
    model: str = "omni-moderation-latest",
    batch_size: int = 32,
) -> CorpusSafetyReport:
    """Check safety for an entire corpus of texts.

    Uses OpenAI's moderation API to screen texts before embedding.
    Filters out content that violates OpenAI's usage policies.

    Args:
        texts: List of texts to check.
        model: OpenAI moderation model identifier.
        batch_size: Number of texts to check per API call.

    Returns:
        CorpusSafetyReport with safety analysis.
    """
    client = get_openai_client()

    all_results: List[SafetyCheckResult] = []
    flagged_indices: List[int] = []

    for i in range(0, len(texts), batch_size):
        chunk = texts[i : i + batch_size]

        response = client.moderations.create(
            input=chunk,
            model=model,
        )

        for j, result_data in enumerate(response.results):
            idx = i + j
            categories = {}
            category_scores = {}

            if hasattr(result_data, 'categories'):
                cats = result_data.categories
                if hasattr(cats, 'model_dump'):
                    cats_dict = cats.model_dump()
                elif hasattr(cats, '__dict__'):
                    cats_dict = vars(cats)
                else:
                    cats_dict = {}
                categories = {k: v for k, v in cats_dict.items() if isinstance(v, bool)}

            if hasattr(result_data, 'category_scores'):
                scores = result_data.category_scores
                if hasattr(scores, 'model_dump'):
                    scores_dict = scores.model_dump()
                elif hasattr(scores, '__dict__'):
                    scores_dict = vars(scores)
                else:
                    scores_dict = {}
                category_scores = {k: v for k, v in scores_dict.items() if isinstance(v, (int, float))}

            result = SafetyCheckResult(
                text=chunk[j],
                flagged=result_data.flagged,
                categories=categories,
                category_scores=category_scores,
                safe_for_embedding=not result_data.flagged,
            )
            all_results.append(result)

            if result_data.flagged:
                flagged_indices.append(idx)

    # Compute summary category counts
    summary_categories: Dict[str, int] = {}
    for result in all_results:
        if result.flagged:
            for cat, is_flagged in result.categories.items():
                if is_flagged:
                    summary_categories[cat] = summary_categories.get(cat, 0) + 1

    flagged_count = len(flagged_indices)
    safe_count = len(texts) - flagged_count

    return CorpusSafetyReport(
        total_texts=len(texts),
        flagged_count=flagged_count,
        safe_count=safe_count,
        flag_rate=flagged_count / len(texts) if texts else 0.0,
        results=all_results,
        flagged_indices=flagged_indices,
        summary_categories=summary_categories,
    )


def filter_safe_texts(
    texts: List[str],
    model: str = "omni-moderation-latest",
) -> Tuple[List[str], List[int]]:
    """Filter corpus to only safe texts, returning safe texts and their original indices."""
    report = check_corpus_safety(texts, model=model)
    safe_texts = [t for t, r in zip(texts, report.results) if r.safe_for_embedding]
    safe_indices = [i for i in range(len(texts)) if i not in report.flagged_indices]
    return safe_texts, safe_indices


def get_safety_summary(
    texts: List[str],
    model: str = "omni-moderation-latest",
) -> Dict[str, Any]:
    """Get a JSON-serializable safety summary for the corpus."""
    report = check_corpus_safety(texts, model=model)
    return {
        "total_texts": report.total_texts,
        "flagged_count": report.flagged_count,
        "safe_count": report.safe_count,
        "flag_rate": report.flag_rate,
        "flagged_categories": report.summary_categories,
        "provider": "OpenAI",
        "moderation_model": model,
        "api_endpoint": "https://api.openai.com/v1/moderations",
    }


if __name__ == "__main__":
    sample_texts = [
        "This is a perfectly safe text about technology.",
        "Machine learning is transforming industries worldwide.",
        "The weather today is sunny and pleasant.",
    ]

    report = check_corpus_safety(sample_texts)
    print(f"Total texts: {report.total_texts}")
    print(f"Safe: {report.safe_count}")
    print(f"Flagged: {report.flagged_count}")
    print(f"Flag rate: {report.flag_rate:.2%}")

    summary = get_safety_summary(sample_texts)
    print(f"\nProvider: {summary['provider']}")
    print(f"API endpoint: {summary['api_endpoint']}")
