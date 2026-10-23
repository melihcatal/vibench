import os
from typing import List, Dict, Any
from openai import OpenAI


def corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Check corpus text for safety concerns before embedding using OpenAI's moderation API.

    Args:
        texts: List of text strings to check

    Returns:
        Dictionary with safety analysis results
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    safety_results = []
    flagged_texts = []

    for i, text in enumerate(texts):
        try:
            # Use OpenAI's moderation endpoint
            response = client.moderations.create(
                model="text-moderation-latest", input=text
            )

            result = response.results[0]
            categories = result.categories
            category_scores = result.category_scores

            # Check if any category is flagged
            is_flagged = result.flagged

            safety_results.append(
                {
                    "text_index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "flagged": is_flagged,
                    "categories": {
                        category: {
                            "flagged": getattr(categories, category),
                            "score": getattr(category_scores, category),
                        }
                        for category in [
                            "harassment",
                            "harassment/threatening",
                            "hate",
                            "hate/threatening",
                            "self-harm",
                            "self-harm/instructions",
                            "self-harm/intent",
                            "sexual",
                            "sexual/minors",
                            "violence",
                            "violence/graphic",
                        ]
                    },
                }
            )

            if is_flagged:
                flagged_texts.append(
                    {
                        "index": i,
                        "text_preview": text[:100] + "..." if len(text) > 100 else text,
                        "reason": [
                            cat
                            for cat in dir(categories)
                            if not cat.startswith("_") and getattr(categories, cat)
                        ],
                    }
                )

        except Exception as e:
            safety_results.append(
                {
                    "text_index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e),
                    "flagged": False,
                }
            )

    # Generate summary
    total_texts = len(texts)
    flagged_count = len(flagged_texts)

    summary = {
        "provider": "openai",
        "moderation_model": "text-moderation-latest",
        "total_texts": total_texts,
        "flagged_texts": flagged_count,
        "flagged_percentage": (flagged_count / total_texts * 100)
        if total_texts > 0
        else 0,
        "safety_summary": "SAFE" if flagged_count == 0 else "CONTAINS_FLAGGED_CONTENT",
        "flagged_details": flagged_texts,
        "detailed_results": safety_results,
    }

    return summary
