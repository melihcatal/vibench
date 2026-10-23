import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Check corpus text for safety issues before embedding using OpenAI's moderation API.

    Args:
        texts: List of text strings to check

    Returns:
        Dict with safety analysis results
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    safety_results = {
        "total_texts": len(texts),
        "flagged_texts": [],
        "safe_texts": [],
        "categories_flagged": set(),
        "overall_safe": True,
    }

    for i, text in enumerate(texts):
        # Skip empty texts
        if not text.strip():
            safety_results["safe_texts"].append(
                {"index": i, "text_preview": "(empty)", "reason": "Empty text"}
            )
            continue

        # Check with OpenAI moderation API
        try:
            response = client.moderations.create(
                model="text-moderation-latest", input=text
            )

            moderation_result = response.results[0]

            if moderation_result.flagged:
                # Extract flagged categories
                flagged_categories = [
                    category
                    for category, flagged in moderation_result.categories.model_dump().items()
                    if flagged
                ]

                safety_results["categories_flagged"].update(flagged_categories)
                safety_results["flagged_texts"].append(
                    {
                        "index": i,
                        "text_preview": text[:100] + "..." if len(text) > 100 else text,
                        "flagged_categories": flagged_categories,
                        "scores": {
                            category: getattr(
                                moderation_result.category_scores, category
                            )
                            for category in flagged_categories
                        },
                    }
                )
                safety_results["overall_safe"] = False
            else:
                safety_results["safe_texts"].append(
                    {
                        "index": i,
                        "text_preview": text[:100] + "..." if len(text) > 100 else text,
                        "reason": "Passed moderation check",
                    }
                )

        except Exception as e:
            # If moderation fails, log error but continue
            safety_results["flagged_texts"].append(
                {
                    "index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e),
                    "flagged_categories": ["moderation_error"],
                }
            )
            safety_results["categories_flagged"].add("moderation_error")
            safety_results["overall_safe"] = False

    # Convert set to list for JSON serialization
    safety_results["categories_flagged"] = list(safety_results["categories_flagged"])

    # Calculate statistics
    safety_results["statistics"] = {
        "percent_flagged": (len(safety_results["flagged_texts"]) / max(len(texts), 1))
        * 100,
        "percent_safe": (len(safety_results["safe_texts"]) / max(len(texts), 1)) * 100,
        "total_flagged": len(safety_results["flagged_texts"]),
        "total_safe": len(safety_results["safe_texts"]),
    }

    # Generate recommendations
    recommendations = []
    if safety_results["flagged_texts"]:
        recommendations.append(
            f"Remove or review {len(safety_results['flagged_texts'])} flagged texts before embedding"
        )
        if "hate" in safety_results["categories_flagged"]:
            recommendations.append("Content contains hate speech - review carefully")
        if "sexual" in safety_results["categories_flagged"]:
            recommendations.append(
                "Content contains sexual material - may not be suitable for all applications"
            )
        if "violence" in safety_results["categories_flagged"]:
            recommendations.append(
                "Content contains violent material - consider content warnings"
            )

    if safety_results["statistics"]["percent_flagged"] > 20:
        recommendations.append(
            "High percentage of flagged content (>20%) - consider reviewing entire corpus"
        )

    safety_results["recommendations"] = recommendations

    return safety_results


def filter_safe_texts(
    texts: List[str], safety_results: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    """
    Filter texts based on safety results.

    Args:
        texts: Original texts
        safety_results: Results from check_corpus_safety

    Returns:
        Tuple of (safe_texts, flagged_texts)
    """
    safe_indices = {item["index"] for item in safety_results["safe_texts"]}

    safe_texts = []
    flagged_texts = []

    for i, text in enumerate(texts):
        if i in safe_indices:
            safe_texts.append(text)
        else:
            flagged_texts.append(text)

    return safe_texts, flagged_texts
