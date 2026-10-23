import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI


def check_corpus_safety(texts: List[str], model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """
    Check corpus text for safety issues before embedding using OpenAI's moderation API.

    Args:
        texts: List of text strings to check
        model: The OpenAI model to use for moderation (default: gpt-4o-mini)

    Returns:
        Dict containing safety analysis results
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    results = {
        "total_texts": len(texts),
        "safe_texts": 0,
        "flagged_texts": 0,
        "flagged_categories": {},
        "text_analyses": [],
    }

    for i, text in enumerate(texts):
        try:
            # Use OpenAI's moderation endpoint
            response = client.moderations.create(
                model="text-moderation-latest", input=text
            )

            moderation_result = response.results[0]
            is_flagged = moderation_result.flagged

            analysis = {
                "text_index": i,
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "is_flagged": is_flagged,
                "categories": moderation_result.categories,
                "category_scores": moderation_result.category_scores,
            }

            results["text_analyses"].append(analysis)

            if is_flagged:
                results["flagged_texts"] += 1

                # Track flagged categories
                for category, flagged in moderation_result.categories.__dict__.items():
                    if flagged:
                        results["flagged_categories"][category] = (
                            results["flagged_categories"].get(category, 0) + 1
                        )
            else:
                results["safe_texts"] += 1

        except Exception as e:
            # Handle API errors
            analysis = {
                "text_index": i,
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "error": str(e),
                "is_flagged": False,
            }
            results["text_analyses"].append(analysis)
            results["safe_texts"] += 1  # Assume safe on error

    # Calculate safety score
    if results["total_texts"] > 0:
        results["safety_score"] = results["safe_texts"] / results["total_texts"]
    else:
        results["safety_score"] = 1.0

    # Generate recommendations
    recommendations = []
    if results["flagged_texts"] > 0:
        recommendations.append(
            f"Found {results['flagged_texts']} texts with safety issues."
        )
        if "harassment" in results["flagged_categories"]:
            recommendations.append(
                "Consider removing or editing texts with harassment content."
            )
        if "hate" in results["flagged_categories"]:
            recommendations.append("Review texts flagged for hate speech.")
        if "self-harm" in results["flagged_categories"]:
            recommendations.append(
                "Texts with self-harm content should be handled carefully."
            )
    else:
        recommendations.append("All texts passed safety checks.")

    results["recommendations"] = recommendations

    return results
