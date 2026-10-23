"""
Check corpus text before embedding using OpenAI Moderation API.
Provider: OpenAI (api.openai.com)
Model: omni-moderation-latest (moderation model)
"""

from typing import List, Dict, Any, Optional

from openai import OpenAI

from embeddings_client import get_openai_client, OPENAI_EMBEDDING_API_HOST


# Provider-specific moderation model identifier
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_text_safety(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> Dict[str, Any]:
    """
    Check if a single text string is safe for embedding using OpenAI Moderation API.

    Args:
        text: The text to check for safety.
        api_key: OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        Dictionary with flagged status, categories, and scores.
    """
    client = get_openai_client(api_key=api_key)

    response = client.moderations.create(
        input=text,
        model=model,
    )

    result = response.results[0]
    flagged = result.flagged

    categories = {}
    category_scores = {}

    if hasattr(result, "categories"):
        for cat_name in result.categories.model_fields:
            cat_value = getattr(result.categories, cat_name, None)
            if cat_value is not None:
                categories[cat_name] = cat_value

    if hasattr(result, "category_scores"):
        for cat_name in result.category_scores.model_fields:
            score_value = getattr(result.category_scores, cat_name, None)
            if score_value is not None:
                category_scores[cat_name] = score_value

    return {
        "text_length": len(text),
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "moderation_model": model,
        "provider": "openai",
        "api_host": OPENAI_EMBEDDING_API_HOST,
    }


def check_corpus_safety(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> List[Dict[str, Any]]:
    """
    Check a corpus of texts for safety before embedding.

    Args:
        texts: List of text strings to check.
        api_key: OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of safety check results for each text.
    """
    results = []
    for i, text in enumerate(texts):
        check_result = check_text_safety(text, api_key=api_key, model=model)
        check_result["index"] = i
        results.append(check_result)

    return results


def filter_safe_texts(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> List[Dict[str, Any]]:
    """
    Filter a corpus, returning only safe texts with their original indices.

    Args:
        texts: List of text strings to filter.
        api_key: OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of dicts with 'index', 'text', and 'safety_check' for safe texts only.
    """
    safety_results = check_corpus_safety(texts, api_key=api_key, model=model)

    safe_texts = []
    for result in safety_results:
        if not result["flagged"]:
            safe_texts.append({
                "index": result["index"],
                "text": texts[result["index"]],
                "safety_check": result,
            })

    return safe_texts


def generate_safety_report(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> str:
    """
    Generate a safety report for a corpus of texts.

    Args:
        texts: List of text strings to analyze.
        api_key: OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        Formatted string report of corpus safety analysis.
    """
    results = check_corpus_safety(texts, api_key=api_key, model=model)

    total = len(results)
    flagged_count = sum(1 for r in results if r["flagged"])
    safe_count = total - flagged_count

    flagged_categories: Dict[str, int] = {}
    for r in results:
        if r["flagged"]:
            for cat_name, is_flagged in r["categories"].items():
                if is_flagged:
                    flagged_categories[cat_name] = flagged_categories.get(cat_name, 0) + 1

    report_lines = [
        "=" * 60,
        "CORPUS SAFETY REPORT (OpenAI Moderation API)",
        "=" * 60,
        f"Provider: OpenAI (api.openai.com)",
        f"Moderation model: {model}",
        f"Total texts analyzed: {total}",
        f"Safe texts: {safe_count}",
        f"Flagged texts: {flagged_count}",
        f"Flag rate: {flagged_count / max(total, 1) * 100:.1f}%",
        "",
        "Flagged Category Breakdown:",
    ]

    if flagged_categories:
        for cat, count in sorted(flagged_categories.items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"  {cat}: {count} occurrences")
    else:
        report_lines.append("  No categories flagged")

    report_lines.append("=" * 60)

    return "\n".join(report_lines)


if __name__ == "__main__":
    sample_corpus = [
        "The weather is nice today.",
        "I love programming in Python.",
        "OpenAI provides great embedding models.",
    ]

    report = generate_safety_report(sample_corpus)
    print(report)
