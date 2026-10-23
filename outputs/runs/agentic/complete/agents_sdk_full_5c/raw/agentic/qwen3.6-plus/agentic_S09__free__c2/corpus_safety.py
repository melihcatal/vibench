"""
[LATER-STEP] Check corpus text before embedding.
Provider: OpenAI Moderation API (api.openai.com, model text-moderation-latest).
"""

from __future__ import annotations

from dataclasses import dataclass

from embeddings_client import get_openai_client
from embeddings_models import chunk_texts


@dataclass
class SafetyResult:
    """Safety assessment for a single text."""
    text: str
    is_safe: bool
    flagged: bool
    categories: dict[str, bool]
    category_scores: dict[str, float]
    index: int


@dataclass
class CorpusSafetyReport:
    """Aggregated safety report for a corpus of texts."""
    results: list[SafetyResult]
    total_texts: int
    safe_count: int
    flagged_count: int
    flagged_indices: list[int]


def check_corpus_safety(
    texts: list[str],
    api_key: str | None = None,
) -> CorpusSafetyReport:
    """
    Check a corpus of texts for safety violations before embedding
    using the OpenAI Moderation API (api.openai.com, model text-moderation-latest).

    Args:
        texts: List of text strings to check.
        api_key: OpenAI API key.

    Returns:
        CorpusSafetyReport with per-text safety assessments.
    """
    client = get_openai_client(api_key=api_key)

    safety_results: list[SafetyResult] = []
    flagged_indices: list[int] = []
    safe_count = 0

    for chunk in chunk_texts(texts, max_chunk_size=32):
        raw_response = client.moderations.create(
            input=chunk,
            model="text-moderation-latest",
        )

        for i, result_item in enumerate(raw_response.results):
            global_idx = chunk_texts(texts).index(chunk) * 32 + i
            is_safe = not result_item.flagged
            categories = dict(result_item.categories)
            category_scores = dict(result_item.category_scores)

            safety_results.append(
                SafetyResult(
                    text=chunk[i],
                    is_safe=is_safe,
                    flagged=result_item.flagged,
                    categories=categories,
                    category_scores=category_scores,
                    index=global_idx,
                )
            )

            if is_safe:
                safe_count += 1
            else:
                flagged_indices.append(global_idx)

    total_texts = len(texts)

    return CorpusSafetyReport(
        results=safety_results,
        total_texts=total_texts,
        safe_count=safe_count,
        flagged_count=len(flagged_indices),
        flagged_indices=flagged_indices,
    )


if __name__ == "__main__":
    sample_corpus = [
        "The weather is beautiful today for a walk in the park.",
        "I love learning new programming languages.",
        "Clean energy solutions help protect our environment.",
    ]
    report = check_corpus_safety(sample_corpus)
    print(f"Total texts checked: {report.total_texts}")
    print(f"Safe: {report.safe_count}, Flagged: {report.flagged_count}")
